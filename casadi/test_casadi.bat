docker run --name casadi_con^
      --user=root^
	  --detach=false^
	  -e DISPLAY=${DISPLAY}^
	  -v /tmp/.X11-unix:/tmp/.X11-unix^
	  --rm^
	  -v %CD%:/mnt/shared^
	  -i^
      -t^
	  casadi /bin/bash -c "cd /mnt/shared && python /mnt/shared/test_casadi.py"