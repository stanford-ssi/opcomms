load 8_autoAlign.csv;
[xi,yi,zi] = interpsurface(X8_autoAlign(:,1),X8_autoAlign(:,2),X8_autoAlign(:,3));
figure
title('Auto Align view');
subplot(2,2,1); title('Speed 8'); surf(xi,yi,zi,'EdgeColor','None');

load 7_autoAlign.csv;
[xi,yi,zi] = interpsurface(X7_autoAlign(:,1),X7_autoAlign(:,2),X7_autoAlign(:,3));
subplot(2,2,2);
title('Speed 7');
surf(xi,yi,zi,'EdgeColor','None');

load 6_autoAlign.csv;
[xi,yi,zi] = interpsurface(X6_autoAlign(:,1),X6_autoAlign(:,2),X6_autoAlign(:,3));
subplot(2,2,3);
title('Speed 6');
surf(xi,yi,zi,'EdgeColor','None');

load 5_autoAlign.csv;
[xi,yi,zi] = interpsurface(X5_autoAlign(:,1),X5_autoAlign(:,2),X5_autoAlign(:,3));
subplot(2,2,4);
title('Speed 5');
surf(xi,yi,zi,'EdgeColor','None');

