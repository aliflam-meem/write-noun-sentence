string = "adsjkskjd lsdk  d wd <start> [sana] <end> sdfnkgfkdsnfk"

start_split_string = string.split("<start>")
end_split_string = start_split_string[1].split("<end>")
print(end_split_string[0])