
%Lissette Wilhelm
%One video for Pinch and another one for Wrap
%K1 K2 Tau Angle1 Angle2 Angle3
%In degrees

close all; clear all; clc;
%Pinch
angles_p = {[1, 1, 1],
    [45, 45, 30],
    [60, 25, 40],
    [90, 5, 15],
    [90, 10, 5]};
k_p = {1, 1;
    1, 1.5;
    2.4, 1.5;
    1.333, 6;
    18, 6;
    9, 18};
%Wrap
angles_w = {[1, 1, 1];
    [45, 45, 30];
    [60, 30, 40];
    [60, 45, 20];
    [90, 15, 30]};
k_w = {1, 1;
    1, 1.5;
    2, 1.5;
    1.333, 3;
    6, 3};

l1 = 0.25;   % length (m)
l2 = 0.25;
l3 = 0.25;

for(i=1:size(angles_p))
    angle = angles_p{i};
    theta1 = deg2rad(angle(1));
    theta2 = deg2rad(angle(2));
    theta3 = deg2rad(angle(3));

    x1_p(i) = (l1/2)*cos(theta1);
    y1_p(i) = (l1/2)*sin(theta1);

    x2_p(i) = l1*cos(theta1) + (l2/2)*cos(theta1+theta2);
    y2_p(i) = l1*sin(theta1) + (l2/2)*sin(theta1+theta2);

    x3_p(i) = l1*cos(theta1) + l2*cos(theta1+theta2) + (l3/2)*cos(theta1+theta2+theta3);
    y3_p(i) = l1*sin(theta1) + l2*sin(theta1+theta2) + (l3/2)*sin(theta1+theta2+theta3);

end


for(i=1:size(angles_w))
    angle = angles_w{i};
    theta1 = deg2rad(angle(1));
    theta2 = deg2rad(angle(2));
    theta3 = deg2rad(angle(3));

    x1_w(i) = (l1/2)*cos(theta1);
    y1_w(i) = (l1/2)*sin(theta1);

    x2_w(i) = l1*cos(theta1) + (l2/2)*cos(theta1+theta2);
    y2_w(i) = l1*sin(theta1) + (l2/2)*sin(theta1+theta2);

    x3_w(i) = l1*cos(theta1) + l2*cos(theta1+theta2) + (l3/2)*cos(theta1+theta2+theta3);
    y3_w(i) = l1*sin(theta1) + l2*sin(theta1+theta2) + (l3/2)*sin(theta1+theta2+theta3);

end

%{
figure('Renderer', 'painters', 'Position', [10 10 900 600])
hold on
for(i=1:length(x1_p))
%i = 1; %1 through 5
    plot([0 x1_p(i)],[0 y1_p(i)],'k-','LineWidth',2);
    plot([x1_p(i) x2_p(i)],[y1_p(i) y2_p(i)],'k-','LineWidth',2)
    plot([x2_p(i) x3_p(i)],[y2_p(i) y3_p(i)],'k-','LineWidth',2)
    plot(x3_p(i), y3_p(i),'bo','MarkerSize',6,'LineWidth',2);
    plot(x2_p(i), y2_p(i),'go','MarkerSize',6,'LineWidth',2);
    plot(x1_p(i), y1_p(i),'ro','MarkerSize',6,'LineWidth',2);
    xlim([-0.2 0.7]);
    ylim([-0.2 0.7]);
    title('Pinch');
    xlabel('X axis (m)');
    ylabel('Y axis (m)');
end
%}
figure('Renderer', 'painters', 'Position', [10 10 900 600])
hold on
for(i=1:length(x1_w))
%i = 1; %1 through 5
    plot([0 x1_w(i)],[0 y1_w(i)],'k-','LineWidth',2);
    plot([x1_w(i) x2_w(i)],[y1_w(i) y2_w(i)],'k-','LineWidth',2)
    plot([x2_w(i) x3_w(i)],[y2_w(i) y3_w(i)],'k-','LineWidth',2)
    plot(x3_w(i), y3_w(i),'bo','MarkerSize',6,'LineWidth',2);
    plot(x2_w(i), y2_w(i),'go','MarkerSize',6,'LineWidth',2);
    plot(x1_w(i), y1_w(i),'ro','MarkerSize',6,'LineWidth',2);
    xlim([-0.2 0.7]);
    ylim([-0.2 0.7]);
    title('Wrap');
    xlabel('X axis (m)');
    ylabel('Y axis (m)');
end