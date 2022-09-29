library(plyr)

# UPDATE WORKING DIRECTORY AS NECESSARY
setwd("/Users/laurasheble/SD_WOS") #you will need to change the filepath on your machine

data <- "SD_WCs_312_noMtgAbstracts_05mar2015data.txt"

df <- read.table(data, na.strings = "na", header=TRUE, sep = "\t", stringsAsFactors=FALSE)
detach(df)
attach(df)

colnames(df)

df[0:10,"UT"]
# create a dataframe with just UT's and WC's
df_wc <- cbind(df["UT"], df["WC"])
# record orig dataframe dimensions to see how many rows
orig_dim <- dim(df_wc)
orig_dim

'''
## now use WCslist to look at list of SCs for each document, add a 1 to the df0 under the appropriate column if present
'''
### My Starter code: SC Extraction ###
# Get list of unique SCs
WCs <- df_wc[,2]
# WCs
WCslist <- lapply(WCs, strsplit, split="; ")
WCunique <- unique(unlist(WCslist, use.names = FALSE))

# Sort alphabetically - this seems pointless - gets turned back later
#     note that apostrophes could be a problem  
WCunique <- sort(WCunique)
# create a dataframe of 0s to add to the original df
df0 <- as.data.frame(matrix(0, ncol=length(WCunique), nrow=nrow(df_wc)))
colnames(df0) <- WCunique

df0 <- sapply(WCunique, function(x) as.integer(grepl(x, WCs)))
# df0
### column bind, minus the original SC field with all SCs
df <- cbind(df_wc[-2],df0)

### END SC Extraction ###Author  PY	Source	Vol	Page	Cites	proportion

### Overview of extracted SCs ###
df[1:2,]
dim(df)

# change to number of rows in my set
# ncol gets the number of columns, the first column is the WOS 'UT' field, which we don't want
col_ct <- ncol(df)
col_ct # 101
no_scsPerDoc <- rowSums(df[2:col_ct]) 
max(no_scsPerDoc) # 7
min(no_scsPerDoc) # 1
mean(no_scsPerDoc) # 2.070513
median(no_scsPerDoc) # 2

### Construct (Symmetric) Adjacency graphs ###
# co-occurrence (adjacency) with documents
df0_co_wc <- df0 %*% t(df0)
# co-occurrence (adjacency) with research areas 
df0_co_wc2 <- t(df0) %*% df0
# above, with 0 on the diagonal:
df0_co_wc2d0 <- df0_co_wc2
diag(df0_co_wc2d0) <- 0
### End adjacency graph construction ###

### Write adjacency matrix to file for use with VosViewer ### 
ints4rownames <- rep(1:dim(df0_co_wc2)[1])
df0_co_wc2_vos <- df0_co_wc2
rownames(df0_co_wc2_vos) <- ints4rownames
write.table(df0_co_wc2_vos, row.names = TRUE, col.names=FALSE, quote=FALSE, sep=",", file ="/Users/laurasheble/SD_WOS/SD_WOS_6mar2015query_WC_adjMatrixdf0_co_wc2_vos.csv")
# generate file of SC names
WC_names_vos <- as.data.frame(rownames(df0_co_wc2))
WC_names_vos <- cbind(as.numeric(ints4rownames), WC_names_vos)
colnames(WC_names_vos) <- (c("id", "Research Field"))
vos_col_names <- (c("id", "label"))
write.table(WC_names_vos, row.names = FALSE, col.names=vos_col_names, sep=",", quote=(2), file ="/Users/laurasheble/SD_WOS/SD_WOS_6mar2015query_WC_adjMatrixdf0_co_wc2_vos_scNames_v2.txt")
length(WC_names_vos)

# NOW WORK IN VOS!
# After working with these in VOSviewer, decided the visuals weren't what I wanted, 
# exported gml format from VOS, imported into Gephi.
# For future, could change output to import directly into Gephi (or Pajek)

