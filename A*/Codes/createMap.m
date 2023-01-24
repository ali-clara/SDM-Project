clear all; 
clc;

R1 = 1;
R2 = 1;
R3 = 1;
Ra = 1;
k1 = 1;
T = [];
i = 1;



 for t1 = linspace(40,90,6)
    for t2 = linspace(10,40,4)
       for t3 = linspace(10,40,4)
          theta1 = deg2rad(t1);
          theta2 = deg2rad(t2);
          theta3 = deg2rad(t3);
          A = [0 0 R1 0;
               theta2 0 R2 0;
               0 theta3 R3 0;
               0 0 0 Ra];
         
          b = [-k1*theta1;0;0;R1*theta1+R2*theta2+R3*theta3];
          
          x = A\b;
          t = transpose(x);
          T(i,:) = [t(1), t(2), t(3), t1, t2, t3];
          i = i + 1;

       end 
    end 

 end 
T1 = array2table(T);
T1.Properties.VariableNames(1:6) = {'K2', 'K3', 'T', 't1', 't2', 't3'};
writetable(T1,'Map_v3shorten.csv')
