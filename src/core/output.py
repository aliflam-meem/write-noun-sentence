def append_string_to_file(string_to_append, file_path):
  """Appends a string to the .txt file.

  Args:
    string_to_append: The string to be appended.
  """
  with open(file_path, 'a', encoding='utf-8') as file:
    file.write(string_to_append + '\n')