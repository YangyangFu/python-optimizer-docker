docker run --name cont^
      --user=root^
	  --detach=false^
	  -e DISPLAY=${DISPLAY}^
	  -v /tmp/.X11-unix:/tmp/.X11-unix^
	  --rm^
	  -v %CD%:/mnt/shared^
	  -i^
      -t^
	  pyomo_ipopt /bin/bash -c "cd /mnt/shared && python /mnt/shared/test_pyomo.py"

