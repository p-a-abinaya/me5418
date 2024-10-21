# CMake generated Testfile for 
# Source directory: /home/abi/turtlebot_rl_ws/src/message_logger
# Build directory: /home/abi/turtlebot_rl_ws/build/message_logger
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_message_logger_gtest_test_message_logger "/home/abi/turtlebot_rl_ws/build/message_logger/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/abi/turtlebot_rl_ws/build/message_logger/test_results/message_logger/gtest-test_message_logger.xml" "--working-dir" "/home/abi/turtlebot_rl_ws/src/message_logger/test" "--return-code" "/home/abi/turtlebot_rl_ws/devel/.private/message_logger/lib/message_logger/test_message_logger --gtest_output=xml:/home/abi/turtlebot_rl_ws/build/message_logger/test_results/message_logger/gtest-test_message_logger.xml")
set_tests_properties(_ctest_message_logger_gtest_test_message_logger PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/noetic/share/catkin/cmake/test/tests.cmake;160;add_test;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;98;catkin_run_tests_target;/opt/ros/noetic/share/catkin/cmake/test/gtest.cmake;37;_catkin_add_google_test;/home/abi/turtlebot_rl_ws/src/message_logger/CMakeLists.txt;103;catkin_add_gtest;/home/abi/turtlebot_rl_ws/src/message_logger/CMakeLists.txt;0;")
subdirs("gtest")
