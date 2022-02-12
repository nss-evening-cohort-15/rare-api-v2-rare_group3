SELECT*
FROM auth_user

DELETE
FROM rare_v2api_comment
where id > 3

SELECT*
FROM rare_v2api_comment

SELECT*
FROM rare_v2api_post

SELECT*
FROM authtoken_token

SELECT* 
FROM rare_v2api_postreaction

INSERT into rare_v2api_postreaction
values (null, 1, 1, 2)
