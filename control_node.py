#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float32
# from geometry_msgs.msg import PoseStamped
# from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import Path
from std_msgs.msg import String
from std_msgs.msg import Bool
from nav_msgs.msg import Path
from std_msgs.msg import Int8
from std_msgs.msg import Float64
from geometry_msgs.msg import Point
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Imu
from io import StringIO
import numpy as np
import sys
import os
import do_mpc
from do_mpc.data import save_results, load_results
from casadi import *
import matplotlib.pyplot as plt
# import matplotlib as mpl
import pickle
sys.path.append('../../')


#def get_bezier_coef(points):
#    n = len(points) - 1

#    # build coefficents matrix
#    C = 4 * np.identity(n)
#    np.fill_diagonal(C[1:], 1)
#    np.fill_diagonal(C[:, 1:], 1)
#    C[0, 0] = 2
#    C[n - 1, n - 1] = 7
#    C[n - 1, n - 2] = 2

#    # build points vector
#    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
#    P[0] = points[0] + 2 * points[1]
#    P[n - 1] = 8 * points[n - 1] + points[n]

#    # solve system, find a & b
#    A = np.linalg.solve(C, P)
#    B = [0] * n
#    for i in range(n - 1):
#        B[i] = 2 * points[i + 1] - A[i + 1]
#    B[n - 1] = (A[n - 1] + points[n]) / 2

#    return A, B


## returns the general Bezier cubic formula given 4 control points
#def get_cubic(a, b, c, d):
#    return lambda t: np.power(1 - t, 3)*a + 3*np.power(1 - t, 2)*t*b + 3*(1 - t)*np.power(t, 2)*c + np.power(t, 3)*d


## return one cubic curve for each consecutive points
#def get_bezier_cubic(points):
#    A, B = get_bezier_coef(points)
#    return [
#        get_cubic(points[i], A[i], B[i], points[i + 1])
#        for i in range(len(points) - 1)
#    ]


#def derivative_bezier(a,b,c,d):
#    return lambda t: np.power(1-t,2)*a*(-3)+3*b*(np.power(1-t,2)-2*t*(1-t))+3*c*(2*t*(1-t)-np.power(t,2))+3*d*np.power(t,2)


#def derivative_list(points):
#    A,B=get_bezier_coef(points)
#    return [derivative_bezier(points[i],A[i],B[i],points[i+1]) for i in range(len(points)-1)]


## evalute each cubic curve on the range [0, 1] sliced in n points
#def evaluate_bezier(points, n):
#    curves = get_bezier_cubic(points)
#    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])


#def trajectory_gen(points):
#    A,B=get_bezier_coef(points)
#    return [get_cubic(points[i],A[i],B[i],points[i+1]) for i in range(len(points)-1)]



class MPController():
    def __init__(self, N_ref = 1):

    	#Model and MPC variables
        self.model_type= 'continuous'
        self.J=1000
        self.La=1
        self.Lb=1
        self.m=200
        self.Cy=0.1
        self.t_s=0.01  # sample time
        self.N=70
        self.k=0.1
        self.N_ref = N_ref


        # variables for control execution
        self.velocities=[1.5]
	    self.path_points=[]
	    self.c=1
	    self.packed=[velocities,c]
	    self.x_initial=[[0],[0],[0],[1.5],[0],[0],[0],[0],[0]]
	    self.x_0 = x_initial

	    #MPC  variables
	    self.model = self.mpc_model()
        self.controller = self.controller(self.model,x_ref,y_ref)
        self.simulator = self.mpc_simulator(self.model,x_ref, y_ref)
        self.estimator = self.do_mpc.estimator.StateFeedback(self.model)

	    # ROS variables
	    self.acc_pub = rospy.Publisher('acceleration', Float32, queue_size=10)
		self.brake_pub = rospy.Publisher('brake', Float32, queue_size=10)
		self.steer_pub = rospy.Publisher('steer', Float32, queue_size=10)
		self.rate=rospy.Rate(10)
		self.vel_sub=rospy.Subscriber("/velocity_plan",Float64MultiArray,self.v_callback)
		self.path_sub=rospy.Subscriber("/A_star_path",Path, self.path_callback)

    def mpc_model(self):
        # Obtain an instance of the do-mpc model class
        model = do_mpc.model.Model(self.model_type)

        # Introduce new states, inputs and other variables to the model, e.g.:
        xc=model.set_variable(var_type='_x',var_name='xc',shape=(1,1))                     # x position
        yc=model.set_variable(var_type='_x',var_name='yc',shape=(1,1))                     # y position
        v=model.set_variable(var_type='_x',var_name='v',shape=(1,1))                       # velocity
        theta=model.set_variable(var_type='_x',var_name='theta',shape=(1,1))               # yaw angle
        phi=model.set_variable(var_type='_x',var_name='phi',shape=(1,1))                   # yaw angular velocity
        delta=model.set_variable(var_type='_x',var_name='delta',shape=(1,1))               # steering angle
        # a_s=model.set_variable(var_type='_x',var_name='a_s',shape=(1,1))                
        # w_s=model.set_variable(var_type='_x',var_name='w_s',shape=(1,1))
        
        # virtual state for timing law
    	z = model.set_variable(var_type='_x', var_name='z', shape = (1,1))
    
        #time varying setpoint for path following
        # target_x = model.set_variable(var_type = '_tvp', var_name = 'target_x', shape = (1,1))
        # target_y = model.set_variable(var_type = '_tvp', var_name = 'target_y', shape = (1,1))
        

        #control inputs
        a=model.set_variable(var_type='_u',var_name='a',shape=(1,1))    # acceleration
        w=model.set_variable(var_type='_u',var_name='w',shape=(1,1))    # steering rate (angular)


        # virtual control input for timing law
  	 	u_v = model.set_variable(var_type='_u',var_name='u_v', shape=(1,1))

        # Set right-hand-side of ODE for all introduced states (_x).
        # Names are inherited from the state definition.
        
        Fyf=self.Cy*(delta-(self.La*phi)/v)
        Fyr=(Cy*self.Lb*phi)/v
        
        equations=vertcat( v*np.sin(theta), 
			               v*np.cos(theta),
			               a_s* np.cos(delta)-(2.0/m)*Fyf*np.sin(delta),
			               phi,
			               (1.0/self.J)*(self.La*(m*a*np.sin(delta)+2*Fyf*np.cos(delta))-2*self.Lb*Fyr),
			               w
			               # ,(1/t_s)*(a-a_s),
			               # (1/t_s)*(w-w_s)
			             )
        
        
        
        model.set_rhs('xc',equations[0])
        model.set_rhs('yc',equations[1])
        model.set_rhs('v',equations[2])
        model.set_rhs('theta',equations[3])
        model.set_rhs('phi',equations[4])
        model.set_rhs('delta',equations[5])
        # model.set_rhs('a_s',equations[6])
        # model.set_rhs('w_s',equations[7])

        #timing law equation
	    timing_law = u_v
	    
	    #RHS of timing law ODEs
	    model.set_rhs('z', timing_law)
	#     model.set_rhs('z[1]', timing_law[1])
	#     model.set_rhs('z[2]', timing_law[2])
	#     model.set_rhs('z[3]', timing_law[3])
	#     model.set_rhs('z[4]', timing_law[4])

        # Setup model:
        model.setup()

        return model

    def controller(self, model, x_ref, y_ref):
        # Obtain an instance of the do-mpc MPC class
        # and initiate it with the model:
        mpc = do_mpc.controller.MPC(model)

        # Set parameters:
        setup_mpc = {
            'n_horizon': self.N,
            't_step': self.t_s,
            'n_robust': 0,
            'open_loop':0,
            'state_discretization': 'collocation',
            'collocation_type': 'radau',
            'collocation_deg': 2,
            'collocation_ni': 2,
            'store_full_solution': True,
        }
        mpc.set_param(**setup_mpc)
        
        #Configuring the time varying behaviour of the setpoints
        
        # tvp_temp = mpc.get_tvp_template()
        # def tvp_fun(t_now):
        #     for k in range(self.N+1):
        #             tvp_temp['_tvp',k,'target_x'] = x_ref[int(t_now//self.t_s) + k]
        #             tvp_temp['_tvp',k,'target_y'] = y_ref[int(t_now//self.t_s) + k]
        #     return tvp_temp
        
        # mpc.set_tvp_fun(tvp_fun)
        
        

        xc = model.x['xc']
	    yc = model.x['yc']
	    z = model.x['z']
	    
	    # Configure objective function:
	    # cost = ((model.x['xc'] - model.tvp['target_x'])/(model.tvp['target_x']+1e-9))**2 + ((model.x['yc'] - model.tvp['target_y'])/(model.tvp['target_y']+1e8) )**2
	    cost = (xc-z)**2 + (yc-y_x(z))**2 + (model.x['v']-v_x(z))**2


        mterm = cost # terminal cost
        lterm = cost # stage cost

        mpc.set_objective(mterm=mterm, lterm=lterm)
        mpc.set_rterm(a=0.00001)
        mpc.set_rterm(w=0.00001) # Scaling for quad. cost.

        # State and input bounds:
     #     mpc.bounds['lower','_x','xc']=x_0[0]-1e-4
     #     mpc.bounds['lower','_x','yc']=y_lower
        mpc.bounds['lower','_x','v']=0 #max reverse speed in m/s
        mpc.bounds['lower','_x','theta']=-50
        mpc.bounds['lower','_x','phi']=-50
        mpc.bounds['lower','_x','delta']=-50
     #     mpc.bounds['upper','_x','xc']=target_x+0.1
     #     mpc.bounds['upper','_x','yc']=y_upper
        mpc.bounds['upper','_x','v']=20 #max forward speed in m/s
        mpc.bounds['upper','_x','theta']=50
        mpc.bounds['upper','_x','phi']=50
        mpc.bounds['upper','_x','delta']=50
        mpc.bounds['lower','_u','a']=-10
        mpc.bounds['lower','_u','w']=-10
        mpc.bounds['upper','_u','a']=10
        mpc.bounds['upper','_u','w']=10
        mpc.bounds['lower','_x','a_s']=-10
        mpc.bounds['lower','_x','w_s']=-10
        mpc.bounds['upper','_x','a_s']=10
        mpc.bounds['upper','_x','w_s']=10

        mpc.setup()

        return mpc

    def mpc_simulator(self, model,x_ref,y_ref):
        # Obtain an instance of the do-mpc simulator class
        # and initiate it with the model:
        simulator = do_mpc.simulator.Simulator(model)

        # Set parameter(s):
        simulator.set_param(t_step = self.t_s)

        # Set function for time-varying parameters.
        # Get the template
        # tvp_temp = simulator.get_tvp_template()

        # Define the function (indexing is much simpler ...)
        # def tvp_fun(t_now):
        #         tvp_temp['target_x'] = x_ref[int(t_now//self.t_s)]
        #         tvp_temp['target_y'] = y_ref[int(t_now//self.t_s)]
        #         return tvp_temp

        # # Set the tvp_fun:
        # simulator.set_tvp_fun(tvp_fun)

        # Setup simulator:
        simulator.setup()

        return simulator

    def control_loop(self, x_ref, y_ref,x_0,i,vel,acc,steer_rate,points,curves,derivatives,velocities,acc_pub,brake_pub,steer_pub):

        ######################################################################################################################################
        '''have to hnge the intial conditions based on new data each time'''
        # x0=np.array([[0],[0],[0.001],[(np.pi/4)*(0.03)],[0],[0],[0],[0]])
        self.simulator.x0['xc'] = 0
        self.simulator.x0['yc'] = 0
        self.simulator.x0['v'] = vel
        self.simulator.x0['theta'] = 0(np.pi/4)*(0.035)
        self.simulator.x0['phi'] = 0
        self.simulator.x0['delta'] = delta
        # simulator.x0['a_s'] = 0
        # simulator.x0['w_s'] = 0

        x_0 = self.simulator.x0.cat.full()

        self.controller.x0 = x_0
        self.estimator.x0 = x_0

        self.controller.set_initial_guess()
        self.controller.reset_history()
        self.simulator.reset_history()
        #######################################################################################################################################
        state = []
        x = []
        y = []
        for k in range(self.N_ref):
            print('\n\n################################################    ' + str(k) + '    #########################################\n\n')
           

            u0 = controller.make_step(x_0)     # 


            if u0[0][0]>=0:
                acc_pub.publish(u0[0][0])
            else:
                brake_pub.publish((-1)*u0[0][0])
            steer_pub.publish(u0[1][0]*t_s)

            y_next = simulator.make_step(u0)
            x_0= estimator.make_step(y_next)

            rospy.spinOnce()
            
        # plt.plot(x,y)
        # plt.plot(x_ref,y_ref-1e-1)
        # plt.plot(x_ref,y_ref+1e-1)
        # plt.plot(x_ref,y_ref)

    def control(x_0,i,x,y,vel,acc,steer_rate,points,curves,derivatives,velocities,acc_pub,brake_pub,steer_pub. x_ref, y_ref):

        fn=curves[i]
        d=derivatives[i]
        vmax_i = 1.5
        # estimator=do_mpc.estimator.StateFeedback(model)

        # Customizing Matplotlib:
        # mpl.rcParams['font.size'] = 18
        # mpl.rcParams['lines.linewidth'] = 3
        # mpl.rcParams['axes.grid'] = True

        # mpc_graphics = do_mpc.graphics.Graphics(mpc.data)
        # sim_graphics = do_mpc.graphics.Graphics(simulator.data)

        # # We just want to create the plot and not show it right now. This "inline magic" supresses the output.
        # fig, ax = plt.subplots(2, sharex=True, figsize=(16,9))
        # fig.align_ylabels()

        # for g in [sim_graphics, mpc_graphics]:
        # # Plot the angle positions (phi_1, phi_2, phi_2) on the first axis:
        # g.add_line(var_type='_x', var_name='xc', axis=ax[0])
        # # g.add_line(var_type='_x', var_name='phi_2', axis=ax[0])
        # # g.add_line(var_type='_x', var_name='phi_3', axis=ax[0])

        # # Plot the set motor positions (phi_m_1_set, phi_m_2_set) on the second axis:
        # g.add_line(var_type='_x', var_name='yc', axis=ax[1])
        # # g.add_line(var_type='_u', var_name='phi_m_2_set', axis=ax[1])

        # ax[0].set_ylabel('X')
        # ax[1].set_ylabel('Y')
        # ax[1].set_xlabel('time [s]')

        # sim_graphics.plot_results()
        # # Reset the limits on all axes in graphic to show the data.
        # sim_graphics.reset_axes()
        # # Show the figure:
        # import time
        # plt.savefig(str(time.time())+'.png')

        for _ in range(N_u):
            u0, x_nxt = self.control_loop(x_ref,y_ref)
            if u0[0][0]>=0:
                acc_pub.publish(u0[0][0])
            else:
                brake_pub.publish((-1)*u0[0][0])
            steer_pub.publish(u0[1][0]*t_s)
            x_0=simulator.make_step(u0)
            # with open('control_outputs.csv',mode='a') as op_file:
            #     op=csv.writer(op_file,delimiter=',')
            #     op.writerow([u0[0][0],u0[1][0]])

            if x_0[1]>=points[i+1][0]:
                break
            # x_0=estimator.make_step(y_0)

        save_results([mpc, simulator])
        with open('results/results.pkl', 'rb') as f:
            results = pickle.load(f)

        print('')
        print('')
        print('='*100)
        print(results['mpc']['_x'])
        print('='*100)
        print('')
        print('')

        os.remove("results/results.pkl")

        acc=vertcat(acc,simulator.data['_u','a',-1])
        x=vertcat(x,simulator.data['_x','xc',-1])
        y=vertcat(y,simulator.data['_x','yc',-1])
        vel=vertcat(vel,simulator.data['_x','v',-1])
        steer_rate=vertcat(steer_rate,simulator.data['_u','omega',-1])
        # z=vertcat(z,simulator.data['_x','theta',-1])

        if x_0[1]>=points[i+1][0]:
            return x_0,x,y,vel,acc,steer_rate
        else:
            # x_0=simulator.data['_x'][-1]
            return control(x_0,i,x,y,vel,acc,steer_rate,points,curves,derivatives,velocities,acc_pub,brake_pub,steer_pub)


	def v_callback(v_arr):
	    print("here")
	 #    velocities.append(v_arr.data[0])
	    # '''l=len(v_arr.data)
	    #             packed[0]=packed[0][:packed[1]]
	    #             for i in range(l):
	    #                 packed[0].append(v_arr.data[i])
	    #             packed[1]+=1'''



	def path_callback(path):
		

	def path_callback(path):
	    vel=packed[0]
	    path_repeat=False
	    x_0=np.zeros((len(x_initial),1))
	    for i in range(len(x_initial)):
	        x_0[i][0]=x_initial[i][0]
	    l = len(path.poses)
	    now_points=np.zeros((l,2))
	    if len(path_points):
	        if path_points[0][0]==path.poses[0].pose.position.y:
	            print("###repetition detected###")
	            path_repeat=True
	            path_sub.unregister()
	            print("#######################################path unregistered#######################################")
	    if not path_repeat:
	        for j in range(l):
	            now_points[j][0]=path.poses[j].pose.position.y-path.poses[0].pose.position.y
	            now_points[j][1]=path.poses[j].pose.position.x-path.poses[0].pose.position.x
	            path_points.append([path.poses[j].pose.position.y,path.poses[j].pose.position.x])
	        x_=np.array([x_0[1]])
	        y_=np.array([x_0[2]])
	        v=np.array([x_0[3]])
	        a=np.array([x_0[7]])
	        s_r=np.array([x_0[-1]])
	        first,rest=now_points[:50,:],now_points[49:,:]
	        while first.shape[0]==50:
	            bcurves=trajectory_gen(first)
	            derivatives=derivative_list(first)

	        #interpolation
	  		# def y_x(x):
			#     return 0.15*np.sin(x*x/25)

			# def v_x(x):
			# 	return 1

	            for i in range(len(first)-1):
	                (x_0,x_,y_,v,a,s_r)=control(x_0,i,x_,y_,
	                	+-v,a,s_r,first,bcurves,derivatives,vel,acc_pub,brake_pub,steer_pub)
	                x_0[0]=0
	            if rest.shape[0]>50:
	                first,rest=rest[:50,:],rest[49:,:]
	            else:
	                break
	        bcurves=trajectory_gen(rest)
	        derivatives=derivative_list(rest)
	        for i in range(len(rest)-1):
	            (x_0,x_,y_,v,a,s_r)=control(x_0,i,x_,y_,v,a,s_r,rest,bcurves,derivatives,vel,acc_pub,brake_pub,steer_pub)
	            x_0[0]=0



	        for i in range(len(x_initial)):
	            x_initial[i][0]=x_0[i][0]
	        fig,ax=plt.subplots(2,2)
	        ax[0][0].plot(x_,y_)
	        ax[0][0].scatter(now_points[:,0],now_points[:,1])
	        ax[0][1].plot(x_,v)
	        ax[0][1].plot(now_points[:,0],vel[:l],'ro')
	        # opt=velocities[:l]
	        for i in range(len(opt)):
	            opt[i]=0.8*opt[i]
	        ax[0][1].plot(now_points[:,0],opt,'bo')
	        ax[1][0].plot(x_,a)
	        ax[1][1].plot(x_,s_r)
	        ax[0][0].set(xlabel='x',ylabel='y')
	        ax[0][1].set(xlabel='x',ylabel='v')
	        ax[1][0].set(xlabel='x',ylabel='a')
	        ax[1][1].set(xlabel='x',ylabel='steer rate')
	        plt.show()



if __name__  = '__main__':
	rospy.init_node('control_node', anonymous=True)
	rate=rospy.Rate(10)
	rospy.spin()
