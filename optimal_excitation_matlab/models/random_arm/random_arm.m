function robot = random_arm()
       
    % degrees of freedom
    robot.dof = 6;
    
    % screws A_i, i-th screw described in i-th frame
    robot.A = [0 0 0 0 0 0 0
               0 0 0 0 0 0 0
               0 0 0 0 0 0 0
               0 0 0 0 0 0 0
               0 0 0 0 0 0 0];
     
    % link frames M_{i,i-1}
    robot.M(:,:,1) = [1  0  0  0
                      0  1  0  0
                      0  0  1  0
                      0  0  0  1];
     
    robot.M(:,:,2) = [1  0  0  0
                      0  0  -1 0
                      0  1  0  0
                      0  0  0  1];
     
    robot.M(:,:,3) = [1  0  0  0
                      0  0  1  0.42
                      0  -1 0  0
                      0  0  0  1];
     
    robot.M(:,:,4) = [1  0  0  0
                      0  0  1  0
                      0  -1 0  0
                      0  0  0  1]; 

    robot.M(:,:,5) = [1  0  0  0
                      0  0  -1 -0.4
                      0  1  0  0
                      0  0  0  1];

    robot.M(:,:,6) = [1  0  0  0
                      0  0  -1 0
                      0  1  0  0
                      0  0  0  1];
     
    
    for i = 1:robot.dof
        robot.M(:,:,i) = inverse_SE3(robot.M(:,:,i));
    end
    
    % joint limits
    robot.q_min = [-2.9671 -2.0944 -2.9671 -2.0944 -2.9671 -3.0543]';
    robot.q_max = [2.9671 2.0944 2.9671 2.0944 2.9671 3.0543]';
    robot.qdot_min = [-1.4835 -1.4835 -1.7453 -1.3090 -2.2689 -2.3562]';
    robot.qdot_max = [1.4835 1.4835 1.7453 1.3090 2.2689 2.3562]';
    

end