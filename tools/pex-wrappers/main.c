
#include <Python.h>

#ifndef PROGRAM
#error You must define PROGRAM for this application to work correctly
#endif

int
main(int argc, char *argv[])
{
  assert(argc >= 1);
  // We need to pass Py_Main an argc/argv that are exactly as if it were the
  // python interpreter. Since we want to execute PROGRAM, this just means
  // giving it an array of size 2 where the second paramter is PROGRAM.
  int py_argc = 2;
  char **py_argv = malloc(py_argc * sizeof(char*));
  py_argv[0] = argv[0];
  py_argv[1] = PROGRAM;
  int result = Py_Main(py_argc, py_argv);
  free(py_argv);
  return result;
}