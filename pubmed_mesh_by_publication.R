require("XML")
require("plyr")
# needed for 'xvalue' function
library("genomes")
library("reshape2")

# UPDATE WORKING DIRECTORY AS NECESSARY
setwd("/path/to/my/directory/of/pubmed_items")#you will need to change the filepath on your machine

# xml="pubmed_sample.xml"  # change file name

doc <- xmlParse(xml)
z <- getNodeSet(doc, "//MedlineCitation")

#####
# return df with one entry per pmid-mesh term combination (long format)

# xvalue in genomes - 1 value

xvalues  <- function(doc, tag, sep ="/"){
  # if wildcard....separate values from different child tags 
  if(grepl( "/\\*$", tag)){
    x <- xpathSApply(doc, tag, xmlValue)
    if(length(x)>0){
      n <- xpathSApply(doc, gsub("/*", "", tag, fixed=TRUE), xmlSize)
      y <-split(x, rep(1:length(n), n))
      names(y) <- NULL
      sapply(y, paste, collapse= sep) 
    }else{ NA}
  }else{
    z <- xpathSApply(doc, tag, xmlValue)
    if(length(z)>0) z
    else NA
  }
}


n<-length(z)
if(n==0){stop("No results found")} 
pubs<-vector("list",n)
for(i in 1:n)
{
  # use xmlDoc or memory leak -see ?getNodeSet for queries on subtree..
  z2<-xmlDoc(z[[i]])  
  pmid    <- xvalue(z2, "/MedlineCitation/PMID")  # first PMID id
  
  mesh <- xvalues(z2, "//DescriptorName")
  # fix for multiple qualifiers in node
  #  mesh <- paste(mesh, collapse="; ")  # one row per pmid
  
  if(! is.na(pmid[1]))  pubs[[i]]<-data.frame(pmid, term=mesh, stringsAsFactors=FALSE)
  
  free(z2)
}
x2<- do.call("rbind", pubs)
x2

#####
# convert to pmid-mesh term matrix (in spirit of document-term matrix)

# create a vector with '1' values, of length of the first dimension of the x2 df
freq = as.vector(rep(1,dim(x2)[1]))
# bind the fequency vector to the x2 df
my_df <- cbind(x2, freq)
# remove commas from mesh terms
gsub( ",", "", as.character(my_df$term))
# prepare to dcast the df: step 1
try_dcast <- melt(my_df, id.vars = "pmid")
# dcast the df: step 2
try_dcast_st2 <- dcast(my_df, pmid ~ term)

# UPDATE FILE NAME, FILE PATH
# write pmid-mesh term matrix to csv (with pipe separator)
write.table(try_dcast_st2,file="mesh_output/pmid_term_matrix_<OR_WHATEVER_filename_is_wanted>.csv",row.names=FALSE,col.names=TRUE, sep="|") # CHANGE FILE NAME!


'''
first Grant entry for a PubmedArticle in pubmed xml
<GrantList CompleteYN="Y">
<Grant>
<GrantID>RFA-HS-05-14</GrantID>
<Acronym>HS</Acronym>
<Agency>AHRQ HHS</Agency>
<Country>United States</Country>
</Grant>
<Grant>
'''


n<-length(z)
if(n==0){stop("No results found")} 
pub_grants<-vector("list",n)
for(i in 1:n)
{
  # use xmlDoc or memory leak -see ?getNodeSet for queries on subtree..
  z2<-xmlDoc(z[[i]])  
  pmid    <- xvalue(z2, "/MedlineCitation/PMID")  # first PMID id  
  gid <- xvalues(z2, "//Grant/GrantID")
  # fix for multiple qualifiers in node
  #  mesh <- paste(mesh, collapse="; ")  # one row per pmid
  gajency <- xvalues(z2, "//Grant/Agency")
  
  if(! is.na(pmid[1]))  pub_grants[[i]]<-data.frame(pmid, grant = paste(gid, gajency, sep = "|", collapse = NULL), stringsAsFactors=FALSE)
  
  free(z2)
}
pub_grants_v2<- do.call("rbind", pub_grants)
head(pub_grants_v2)
write.table(pub_grants_v2,file="mesh_output/pmid_grant_matrix_<OR_WHATEVER_filename_is_wanted>.csv",row.names=FALSE,col.names=TRUE, sep="|") # CHANGE FILE NAME!

# create a vector with '1' values, of length of the first dimension of the pub_grants df
freq = as.vector(rep(1,dim(pub_grants_v2)[1]))
# bind the fequency vector to the pub_grants df
pub_grantsf <- cbind(pub_grants_v2, freq)
# prepare to dcast the df: step 1
g_dcast <- melt(pub_grantsf, id.vars = "pmid")
# dcast the df: step 2
g_dcast_st2 <- dcast(pub_grantsf, pmid ~ grant)

# UPDATE FILE NAME, FILE PATH
# write pmid-mesh term matrix to csv (with pipe separator)
write.table(g_dcast_st2,file="mesh_output/pmid_grant_matrix_<OR_WHATEVER_filename_is_wanted>_wideFormat_20141029.csv",row.names=FALSE,col.names=TRUE, sep="|") # CHANGE FILE NAME!


#################
# exploring helper: to see hom many pmids, mesh terms per article

mlen <- function (doc, tag){
  n <- xpathSApply(doc, tag, xmlValue)
  if (length(n) >0)
    length(n)
  else NA
}

z <- getNodeSet(doc, "//MedlineCitation")
n <-length(z)
articles <-vector("list",n)
for(i in 1:n)
{
  z2<-xmlDoc(z[[i]])
  articles[[i]] <- data.frame(if(! is.na(pmid[1]))
    # Need to specify which PMID because additional PMIDs for related articles are listed in MedlineCitation
    PMID = mlen(z2, "/MedlineCitation/PMID"),
    #    PMID = xpathSApply(doc, "/PubmedArticle/MedlineCitation/PMID", xmlValue),
    GRANT_ID = mlen(z2, "//GrantID"),
    stringsAsFactors=FALSE)
    
  free(z2)  
}
x_len <- do.call("rbind", articles)
dim(x_len)

############
# not used for final version: extract pmid, mesh terms, returns df with one pmid, string of mesh terms concatenated with '; ' per row


xp <- function (doc, tag){
  n <- xpathSApply(doc, tag, xmlValue)
  if (length(n) > 0) 
    # paste multiple values?  BILCOD and probably others..
    paste0(n, collapse="; ") 
  else NA
}

z <- getNodeSet(doc, "//MedlineCitation")
n <-length(z)
articles <-vector("list",n)
for(i in 1:n)
{
  z2<-xmlDoc(z[[i]])
  articles[[i]] <- data.frame(
# Need to specify which PMID because additional PMIDs for related articles are listed in MedlineCitation
    PMID = xp(z2, "/MedlineCitation/PMID"),
#    PMID = xpathSApply(doc, "/PubmedArticle/MedlineCitation/PMID", xmlValue),
    MESH = xp(z2, "//DescriptorName"),
    stringsAsFactors=FALSE)
  free(z2)  
}
x <- do.call("rbind", articles)
head(x)
dim(x)

