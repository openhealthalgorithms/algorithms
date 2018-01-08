function [WHOcvdRisk] = generateWHOriskScore(c1,c2,c3,c4,c5, ii, jj)

% Function generateWHOriskScore() retrieves the 10-year CVD risk using 
% the WHO/ISH CVD risk prediction charts for South East Asian Regions D (SEAR D).
% It takes 7 parameters (described below) as 
% input, and subsequently generates a string that will pull the relevant 
% file having the 10-year WHO/ISH CVD risk score. Parameter c1 determines 
% whether the High Information (HI) model or Low Information (LI) model 
% is used to estimate risk.
% Input parameters-
% c1 - cholesterol information present ? ('c' - yes; 'uc'- no)
% c2 - diabetes status ? ('d' - present; 'ud' - not detected/absent)
% c3 - gender ? ('m' - male; 'f' - female)
% c4 - smoker ? ('s' - smoker; 'ns' - non-smoker)
% c5 - age (discretised; 40,50,60,70);
% ii - SBP (discretised, in mmHg; 1 (SBP-180), 2 (SBP-160), 3 (SBP-140), 4 (SBP-120))
% jj - CHOL (0 if 'uc';if 'c', then discretised (in mmol/L) to
%         1 (TC 3-<4), 2 (TC 4-<5), 3 (TC 5-<6), 4 (TC 6-<7), 5 (TC 7-<8) ) 
% Returns-
% 10-year CVD risk as per SEAR-D WHO/ISH risk prediction charts
%
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
    

var=strcat(c1,'_',c2,'_',c3,'_',c4,'_',num2str(c5));
y=strcat(path,var,'.txt');
%disp(y) %display file accessed
M = dlmread(y);
%OPTIONAL - display risk if need be
if(M(ii,jj)==10);
  %  disp('CVD risk <10%');    
elseif(M(ii,jj)==20);
  %  disp('CVD risk 10% to <20%');
elseif(M(ii,jj)==30);
  %  disp('CVD risk 20% to <30%');
elseif(M(ii,jj)==40);
  %  disp('CVD risk 30% to <40%');
elseif(M(ii,jj)==50);
  %  disp('CVD risk is >40%');
end
WHOcvdRisk = M(ii,jj);
end