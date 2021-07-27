clear;close all; clc

load('SMEARII/smear2.mat');
DATA1 = final; clear final

% https://www.mathworks.com/help/matlab/ref/writetimetable.html
writetimetable(DATA1,'SMEARII/SMEAR2.xlsx','Sheet',1) 