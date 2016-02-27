function [xi,yi,zi] = interpsurface(a,b,c)
    %figure
    cSmooth = [2:length(a)-1];
    for i = 2:length(a)-1 
        cSmooth(i) = (mean([c(i-1), c(i), c(i+1) ]));
    end
    [xi,yi] = meshgrid(a(2:length(a)) , b(2:length(a)));
    zi = griddata(a(2:length(a)),b(2:length(a)),cSmooth,xi,yi);
    %[xi,yi] = meshgrid(a, b);
    %zi = griddata(a,b,c,xi,yi);
    %surf(xi,yi,zi,'EdgeColor','None');
end
