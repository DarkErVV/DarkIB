#DATABASE

##Image
* id - usigned bigint, uniq index
* md5_hash - text
* size - int, kb
* height - int
* width - int
* type - 0: gif, 
         1: png,
         2: jpg,  
* uid - foreigh key, int, id uploaded user


##Tags
* id - int, index,
* name
* type (char name, author, title,  etc)
