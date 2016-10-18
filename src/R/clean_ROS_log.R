
# Script use to clean text files created by ROS Log function during execution
# of roslaunch commandline to control a robot.
# The output of this script was used as input of a Matlab script to plot
# the path following over the graphic of grid mapping
#

removeString <- function(x){
    mf = matrix(data=NA, nrow = nrow(x), ncol = ncol(x))
    colnames(mf) <- colnames(x)
    for(colname in colnames(x)){
        xm = as.matrix(x[,colname])
        #print( xm)
        df = data.frame(strsplit(xm, ":"))
        for(i in 1:nrow(x)){
            str = array(df[2,i])
            n = as.numeric(str)
            mf[i,colname] = n
        }
    }
    return(mf)
}

# file name
fname = "2016-09-28-23-37-02"
spath = "D:/IoT/Robot_Project/bag/"
path_csv = sprintf("D:/IoT/Robot_Project/bag/%s.csv", fname)
path_txt = sprintf("D:/IoT/Robot_Project/bag/%s.txt", fname)
strToRemove <- c("time:", "omega:", "v:", "w:", "x_est[0]:", "x_est[1]:", "x_est[2]:", "goal[0]:", "goal[1]:")
pi <- read.csv(path_txt, header = FALSE, sep = ',')
m <- pi[c(2,4,5,6,8,9,10,11,12)]
# colnames(m) <- c("TIME","OMEGA","V","W","X","Y","THETA","G1","G2")
# start to remove strings
mclean <- removeString(m)
sf1 = sprintf("%sout-%s.txt",spath,fname)
sf2 = sprintf("%sout-%s.csv",spath,fname)
write.table(mclean, file=sf1, sep=",", row.names = FALSE, col.names = FALSE, dec=".")
write.csv2(mclean, file=sf2, dec = ".", row.names = FALSE)




