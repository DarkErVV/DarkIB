## DATABASE
### Tables:

### Image
| Name | Type | Discription |
| -----| :---:| :-----------|
| id | usigned bigint | uniq index
| md5_hash | text| |
| size | int| file size in kb |
| height | int | pixels |
| width | int | pixels  |
| type | smallint | 0: gif, 1: png,   2: jpg,|
| uid  | foreigh key, int| id uploaded user |
|date_upload| datatime | 

### Tags
| Name | Type | Discription |
| -----| :---:| :-----------|
| id  | int| uniq index|
| name | text | tag name |
| type | text? | tag type (character name, author, title, or etc)|

### TAG - PIC
| Name | Type | Discription |
| -----| :---:| :-----------|
| id_tag | int ||
| id_pic | int ||

### Users
| Name | Type | Discription |
| -----| :---:| :-----------|
| user_id| int(11) |||
| username| varchar(20) ||
| password |varchar(10)||
| email|varchar(50)||
| registred_on |datetime)||
