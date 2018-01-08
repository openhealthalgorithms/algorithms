% Example implementation to find the 10-year cardiovascular disease (CVD)
% risk score using input variables (demographics, risk factors) via
% the WHO/ISH CVD risk prediction charts for SEAR-D.
% Implemented by Arvind Raghu, Oxford University, 2013
%
% Last updated at 17:26 on 19-02-2015 by Arvind Raghu
% ********************************************************************
% If you find this code useful, please cite:
%
%  A.Raghu et al.: Evaluating cardiovascular disease risk using the
%  WHO/ISH risk prediction charts for South East Asian Regions D (2015)
%                               OR
%  A. Raghu et al.: Engineering a mobile health tool for resource-poor
%  settings to assess and manage cardiovascular disease risk: SMARThealth
%  study (2015)
% ********************************************************************
%
% Send queries/suggestions/bug reports/a hi to say if it's useful to
% <email@arvindraghu.com>
% --------------------------------------------------------------------
%    This program is free software; you can redistribute it and/or modify
%    it under the terms of the GNU General Public License as published by
%    the Free Software Foundation; either version 2 of the License, or
%    (at your option) any later version.
%
%    This program is distributed in the hope that it will be useful,
%    but WITHOUT ANY WARRANTY; without even the implied warranty of
%    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%    GNU General Public License for more details.
%
%    You should have received a copy of the GNU General Public License
%    along with this program; if not, write to the Free Software
%    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
%--------------------------------------------------------------------------

%Set path
path='/Users/fredhersch/Development/cvdrisk/WHOfiles/';
addpath(path)
%% Example 1
% Given a female patient in India aged 65 years,non-smoker with BP 141/85 and
% having diabetes. The total cholesterol was recorded to be 5.4 mmol/L.

%% Step1: Determine parameter ranges
p1_age = 65;
p1_gender =2;
p1_sbp = 141;
p1_smoker = 0;
p1_tc_info = 1; %change to 0 if no TC info available (i.e.use LI charts)
p1_tc = 5.4;    %change to 0 if no TC info available (i.e.use LI charts)
p1_diabetes = 1;

%cholesterol status
if (p1_tc_info==1)
    c1='c';
else
    c1='uc';
end
%diabetes status
if (p1_diabetes==1)
    c2='d';
elseif (p1_diabetes==0)
    c2='ud';
end
%gender
if (p1_gender==1)
    c3='m';
elseif (p1_gender==2)
    c3='f';
end
%smoking status
if (p1_smoker==1)
    c4='s';
elseif (p1_smoker==0)
    c4='ns';
end

if(p1_age>=18 && p1_age<40)
    c5=40;
elseif(p1_age>=40 && p1_age<50)
    c5=40;
elseif(p1_age>=50 && p1_age<60)
    c5=50;
elseif(p1_age>=60 && p1_age<70)
    c5=60;
elseif(p1_age>=70 && p1_age<80)
    c5=70;
elseif(p1_age>=80) %threshold adjustable according to clinical judgement
    c5=70;
end

if(p1_sbp>169.9) %threshold adjustable according to clinical judgement
    ii=1;
    % disp('180');
elseif(p1_sbp>149.9 && p1_sbp<=169.9)
    ii=2;
    % disp('160');
elseif(p1_sbp>129.9 && p1_sbp<=149.9)
    ii=3;
    % disp('140');
elseif(p1_sbp<=129.9)
    ii=4;
    % disp('120');
end
if (p1_tc<=4.50 ) %threshold adjustable according to clinical judgement
    jj=1;
    % disp('4');
elseif (p1_tc>4.50 && p1_tc<=5.50)
    jj=2;
    % disp('5');
elseif (p1_tc>5.50 && p1_tc<=6.50)
    jj=3;
    % disp('6');
elseif (p1_tc>6.50 && p1_tc<=7.50)
    jj=4;
    % disp('7');
elseif (p1_tc>7.50)
    jj=5;
    % disp('8');
end

%% Step2: Determine CVD risk
%Use function generateWHOriskScore to get 10-year risk
result=generateWHOriskScore(c1,c2,c3,c4,c5, ii, jj);

%interpret result
if(result==10)
    disp('10-year CVD risk <10%');
elseif(result==20)
    disp('10-year CVD risk 10% to <20%');
elseif(result==30)
    disp('10-year CVD risk 20% to <30%');
elseif(result==40)
    disp('10-year CVD risk 30% to <40%');
elseif(result==50)
    disp('10-year CVD risk >40%')
else
    disp('Risk cannot be calculated');
end
