%% 读入螺纹图片，图片拍的是螺纹下部，所以牙顶和牙底正好相反
clear;clc;
close all
%pixel_org=imread('Image_20230213163035800.bmp');
%pixel_org=imread('Image_20230213163032812.bmp');            
%pixel_org=imread('Image_20230213163040450.bmp');
%pixel_org=imread('Image_20230213163031818.bmp');
%pixel_org=imread('Image_20230213163035469.bmp');
%pixel_org=imread('Image_20230213163039122.bmp');
%pixel_org=imread('Image_20230213163039286.bmp');
%pixel_org=imread('Image_20230213163031487.bmp');
pixel_org=imread('Image_20230213163031653.bmp');
%pixel_gray=rgb2gray(pixel_org);
figure
imshow(pixel_org)
title('螺纹原图')
%% 对螺纹图片进行滤波处理, 并执行边缘检测
I=medfilt2(pixel_org,[5,5]);                                % 中值滤波把原图里的噪声点滤去
se=strel('square',30);                                      % 结构元素
I=imclose(I,se);                                            % 闭运算
pixel_contour=edge(I,'canny',[0.1 0.3]);                    % 边缘检测, 得到螺纹的轮廓波形
[m,n]=size(pixel_contour);                                   % 计算图像的尺寸
pixel_contour=pixel_contour(500:m-1037,500:n-1025);         % 把图像的边角去掉, 仅留下有用的部分
[m,n]=size(pixel_contour);                                  % 计算去掉边角之后的图像尺寸
imwrite(pixel_contour,'螺纹波形.png')
imshow(pixel_contour)                                       % 显示轮廓图
title('螺纹波形')
%% 提取轮廓图像素点的坐标
N=1;   % 计数器
I=pixel_contour;
for i=1:m               
    for j=1:n
        if I(i,j)==1      
            y(N)=i;                                         % 保存白色像素的横坐标 x
            x(N)=j;                                         % 保存白色像素的纵坐标 y
            N=N+1;                                          % 计数器 +1
        end
    end
end
[x,IX]=sort(x);                                             % x数组按升序排列
y=y(IX);                                                    % 对应的y数组顺序依次和x对应
pixelX=x;pixelY=y;                                          % 保存像素点
%% 查找牙顶
search_range1=size(y,2);                                    % 确定搜索范围，初始范围是整个y数组
N=1;
gamma=n;                                                    % 寻找到的牙顶的坐标，初始值为n
while(gamma>300)                                            % 当牙顶位置坐标小于300时，停止搜索
    IY=find(y(1:search_range1)==max(y(1:search_range1)));   % 查找牙顶在y数组里的位置
    mean_top(1,N)=x(round(mean(IY)));                       % 得到平均峰顶位置，是x数组的内容(真实的像素横坐标）,mean_top存放牙顶位置的数组
    search_range1=max(find(x==mean_top(1,N)-100));          % 将像素横坐标左推100，找到在数组的位置，作为在y数组下一次寻找牙顶的搜索范围
    gamma=mean_top(1,N);                                    %
    N=N+1;
end
top_num=size(mean_top,2)                                    %牙顶数量
%% 构造顶点ROI1
map=zeros(top_num,n);                                       % ROI掩码矩阵赋初值
for i=1:top_num                                             % 逐行设置
    for j=(max(1,mean_top(i)-40):min(mean_top(i)+40,n))     % 扩展顶点范围以备polyfit
        map(i,j)=1;
    end
end
for i=1:top_num
    ROI1(:,:,i)=repmat(map(i,:),m,1).*pixel_contour;        % 取感兴趣区
    imwrite(ROI1(:,:,i),'1.png')                            % ?如何输出变化的文件名？
end
%% 查找牙底
search_range2=1;                                            % 确定搜索范围，初始值是整个y数组
N=1;
gamma=1;
while(n-gamma>300)
    IY1=find(y(search_range2:size(y,2))==min(y(search_range2:size(y,2))));    % 查找牙底在y数组里的位置,因为是搜索范围后移，找到的为相对地址
    IY1=IY1+search_range2-1;                                % 转换为绝对地址
    mean_bottom(1,N)=x(round(mean(IY1)));                   % 得到平均牙底位置
    search_range2=min(find(x==mean_bottom(1,N)+100));       % 下一次寻找牙底的搜索起点
    gamma=mean_bottom(1,N);
    N=N+1;
end
bottom_num=size(mean_bottom,2)
%% 构造牙底ROI2
map1=zeros(bottom_num,n);                                   % ROI掩码矩阵赋初值
for i=1:bottom_num                                          % 逐行设置
    for j=(max(1,mean_bottom(i)-40):min(mean_bottom(i)+40,n))           % 扩展牙底范围以备polyfit
        map1(i,j)=1;
    end
end
for i=1:bottom_num
    ROI2(:,:,i)=repmat(map1(i,:),m,1).*pixel_contour;       % 取感兴趣区
    %imwrite(ROI2(:,:,i),'2.png')                            % ?如何输出变化的文件名？
end
%% 多项式拟合顶点和底点
for i=1:top_num
    [x_curve,y_curve]=find(ROI1(:,:,i)==1);                 % 拟合牙顶
    a(i,:)=polyfit(y_curve,x_curve,2);                      % 二次曲线拟合
    f=polyval(a(i,:),y_curve);
    scatter(y_curve,x_curve)
    hold on
    plot(y_curve,f)
    
end
for i=1:bottom_num
    [x_curve1,y_curve1]=find(ROI2(:,:,i)==1);               % 拟合牙底
    b(i,:)=polyfit(y_curve1,x_curve1,2);                    % 二次曲线拟合
    f1=polyval(b(i,:),y_curve1);
    scatter(y_curve1,x_curve1)
    hold on
    plot(y_curve1,f1)
end
%% 求顶点和底点坐标
for i=1:top_num                                         
    top(i,1)=-a(i,2)/2/a(i,1);
    top(i,2)=(4*a(i,1)*a(i,3)-a(i,2)^2)/4/a(i,1);
end
for i=1:bottom_num
    bottom(i,1)=-b(i,2)/2/b(i,1);
    bottom(i,2)=(4*b(i,1)*b(i,3)-b(i,2)^2)/4/b(i,1);
end
%% 构造顶点两边斜坡ROI
map2=zeros(2,n);                                            % ROI掩码矩阵赋初值
peak=mean_top(round(top_num/2));                            % 取中间牙顶
for j=(peak-50-70):(peak-50)                                % 左坡范围，峰顶以下50像素截取70像素长
    map2(1,j)=1;
end
for j=(peak+50):(peak+50+70)                                % 右坡范围，峰顶以下50像素截取70像素长
    map2(2,j)=1;
end
ROI2=repmat(map2(1,:),m,1).*pixel_contour;
ROI3=repmat(map2(2,:),m,1).*pixel_contour;
imwrite(ROI2,'ROI2.png')
imwrite(ROI3,'ROI3.png')
%% 直线拟合左右牙坡
[x_curve2,y_curve2]=find(ROI2==1);                          % 
    left_slope=polyfit(y_curve2,x_curve2,1);                % 用polyfit一次拟合，斜率和截距在left_slope
    f_left_slope=polyval(left_slope,y_curve2);
    scatter(y_curve2,x_curve2)
    hold on
    plot(y_curve2,f_left_slope)
[x_curve3,y_curve3]=find(ROI3==1);                          % 
    right_slope=polyfit(y_curve3,x_curve3,1);               % 用polyfit一次拟合，斜率和截距在right_slope
    f_right_slope=polyval(right_slope,y_curve3);
    scatter(y_curve3,x_curve3)
    hold on
    plot(y_curve3,f_right_slope)

%% 分别对牙顶和牙底, 执行直线拟合, 得到螺纹轮廓的两条包络线
top_fit=polyfit(top(:,1),top(:,2),1);
bottom_fit=polyfit(bottom(:,1),bottom(:,2),1);
x0=[1 n];
y1=top_fit(1)*x0+top_fit(2);
y2=bottom_fit(1)*x0+bottom_fit(2);
plot(x0,y1,'r',x0,y2,'b')





    







