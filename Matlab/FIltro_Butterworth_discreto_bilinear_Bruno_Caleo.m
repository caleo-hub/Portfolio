%>>>>>>>> IMPLEMENTAÇÃO DE FITROS DIGITAIS
%>>>> 2ª Projeto

clear all 
clc
close all



format long
Wc=2*pi/3;
Fs=1;
Wn=2*Fs*tan(Wc/2); %Pre Warping
[B1,A1] = butter(6,Wn,'s');
[B1d,A1d] = bilinear(B1,A1,Fs);
direta = dfilt.df1(B1d,A1d);
cascata=sos(direta);
cascata_aux=cascata;

freqz(direta);
title('Magnitude Response and Phase Response (Forma Direta)')
legend('Magnitude','Fase')


freqz(cascata);
title('Magnitude Response and Phase Response (Forma Cascata)')
legend('Magnitude','Fase')



%>>>>>>SENSIBILIDADE À QUATIZAÇÃO DOS PARÂMETROS

i=12;
bi = round(B1d,i);
ai = round(A1d,i);
direta_dec = dfilt.df1(bi,ai);
cascata_aux.sosMatrix=round(cascata.sosMatrix,i);
cascata_aux.ScaleValues=round(cascata.ScaleValues,i);
freqz(direta_dec)
title('Magnitude Response and Phase Response (Forma Direta com 12 casa decimais)')
legend('Magnitude','Fase')
freqz(cascata_aux)
title('Magnitude Response and Phase Response (Forma Cascata com 12 casa decimais)')
legend('Magnitude','Fase')

i=8;
bi = round(B1d,i);
ai = round(A1d,i);
direta_dec = dfilt.df1(bi,ai);
cascata_aux.sosMatrix=round(cascata.sosMatrix,i);
cascata_aux.ScaleValues=round(cascata.ScaleValues,i);
freqz(direta_dec)
legend('Magnitude','Fase')
title('Magnitude Response and Phase Response (Forma Direta com 8 casa decimais)')
freqz(cascata_aux)
title('Magnitude Response and Phase Response (Forma Cascata com 8 casa decimais)')
legend('Magnitude','Fase')

i=4;
bi = round(B1d,i);
ai = round(A1d,i);
direta_dec = dfilt.df1(bi,ai);
cascata_aux.sosMatrix=round(cascata.sosMatrix,i);
cascata_aux.ScaleValues=round(cascata.ScaleValues,i);
freqz(direta_dec)
legend('Magnitude','Fase')
title('Magnitude Response and Phase Response (Forma Direta com 4 casa decimais)')
freqz(cascata_aux)
title('Magnitude Response and Phase Response (Forma Cascata com 4 casa decimais)')
legend('Magnitude','Fase')
