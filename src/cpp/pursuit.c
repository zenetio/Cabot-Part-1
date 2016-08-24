	double STEP_TIME = 0.1;
	double SCALE_P = 1.0;
	double SCALE_V = 8.0;
	double WP_DIST = 30.0;
	double FOLLOW_DIST = 50.0;
	int X_OFF = 0;
	int Y_OFF = 0;
	int CRUMB_SZ = 500;
	int NUM_WP=5;
	int X = 0;
	int Y = 1;
	int DIM = 2;

	boolean isStart = false;

	int sim_counter = 0;
	double sim_t = 0.0;
	double sim_v = 0.0;
	double sim_d = 0.0;
	double sim_xp = 0.0;
	double sim_yp = 0.0;
	double sim_xv = 0.0;
	double sim_yv = 0.0;

	double steer_fx = 0.0;
	double steer_fy = 0.0;

	double[][] way_pts = {{300.0,500.0},{100.0, 500.0},{100.0,100.0}, {500.0,100.0},{500.0, 500.0}};
	int cur_way_pt = 0;

	double[][] crumbs = new double[CRUMB_SZ][DIM];
	int crumb_idx = 0;

	void setPosition(double x, double y) {
	  sim_xp = x;
	  sim_yp = y;
	}
	void setVelocity(double val) {
	  sim_v = val;
	}
	void setSteering(double val) {
	  sim_d = val;
	}
	void changeSteeringBy(double delta) {
	  sim_d += delta;
	}
	void setFollow(double x, double y) {
	  steer_fx = x;
	  steer_fy = y;
	}
	int getCurrentWaypoint() {
	  return cur_way_pt;
	}
	int getPreviousWaypoint() {
	  int pwp = (cur_way_pt==0)?(NUM_WP-1):cur_way_pt-1;
	  return pwp;
	}

	void setup() {
	  size(600, 600);
	  initSim();
	}

	void draw() { 
	  background(240);
	 
	  if (isStart) {
		updateSim();
		updateSteering(sim_xp, sim_yp, sim_d);
		updateWaypoint(sim_xp, sim_yp);
		updatePursuit(sim_xp, sim_yp);
		updateCrumbs(sim_xp, sim_yp);
		updateRover();
	  }
		
	  drawCrumbs();
	  drawWayPoints();
	  drawRover();
	  drawPursuit();
	  
	  delay(1);
	}

	void initSim() {
	  cur_way_pt=1;
	  setFollow(280.0, 500);
	  setPosition(300.0, 400.0);
	  setVelocity(1.5);
	  setSteering(4);
	  updateRover();
	}

	void updateSim() {
	  sim_counter++;
	  sim_t += STEP_TIME;
	  if ((sim_counter % 20) == 0) {
		sim_d += random(-0.2, 0.2);
		sim_xp += random(-1.5, 1.5);
		sim_yp += random(-1.5, 1.5);
	  }
	}  

	void updateSteering(double x, double y, double dir) {
	  double fdx = (x-steer_fx);
	  double fdy = (y-steer_fy);  
	  double fdist = calcDist(fdx, fdy);
	  
	  // Compute the cross product -- tells which way to turn
	  double cdir = cos((float)dir);
	  double sdir = sin((float)dir);
	  double xprod = (sdir*fdx - cdir*fdy)/fdist;
	  
	  double val = 0.0;
	  if (xprod < -0.1) val = 0.06;
	  else if (xprod > 0.1) val = -0.06;
	  changeSteeringBy(-val);
	}

	void updateWaypoint(double x, double y) {
	  double cwpx = way_pts[cur_way_pt][X];
	  double cwpy = way_pts[cur_way_pt][Y];
	  double cdist = calcDist(x-cwpx, y-cwpy);
	  
	  if (cdist < WP_DIST) cur_way_pt++;
	  if (cur_way_pt >= NUM_WP) cur_way_pt = 0;
	}

	void updatePursuit(double x, double y) {
	  double fdist = calcDist(x-steer_fx, y-steer_fy);  
	  if (fdist < FOLLOW_DIST) {
		int cwp = getCurrentWaypoint();
		int pwp = getPreviousWaypoint();
		double wpx = way_pts[cwp][X] - way_pts[pwp][X];
		double wpy = way_pts[cwp][Y] - way_pts[pwp][Y];
		double wpdist = calcDist(wpx, wpy);
		double cdist = calcDist(x-way_pts[cwp][X], y-way_pts[cwp][Y]);
		
		double wp_ratio = (wpdist - cdist + FOLLOW_DIST)/wpdist;
		if (wp_ratio > 1.0) wp_ratio = 1.0;
		
		double nx = way_pts[pwp][X] + wp_ratio*wpx;
		double ny = way_pts[pwp][Y] + wp_ratio*wpy;
		setFollow(nx, ny);
	  }
	}

	void updateCrumbs(double x, double y) {
	  if ((sim_counter % 3) == 0) {
		crumbs[crumb_idx][X] = sim_xp;
		crumbs[crumb_idx][Y] = sim_yp;
		crumb_idx++;
		if (crumb_idx >= CRUMB_SZ) crumb_idx = 0;
	  }
	}

	void updateRover() {
	  sim_xv = sim_v*cos((float)sim_d);
	  sim_yv = sim_v*sin((float)sim_d);
	  sim_xp += sim_xv;
	  sim_yp += sim_yv;
	}

	void drawRover() {
	  float x = calcDrawX(sim_xp);
	  float y = calcDrawY(sim_yp);
	  float xd = x + calcDrawV(sim_xv);
	  float yd = y + calcDrawV(sim_yv);
		
	  stroke(0);
	  fill(250, 0, 0);
	  ellipse(x, y, 10, 10);
	  stroke(0, 0, 200);
	  line(x, y, xd, yd);
	}

	void drawPursuit() {  
	  stroke(180);
	  float nx = calcDrawX(steer_fx);
	  float ny = calcDrawY(steer_fy);
	  float d = calcDraw(2*FOLLOW_DIST);
	  fill(0, 250, 0);
	  ellipse(nx, ny, 5, 5);
	  noFill();
	  ellipse(nx, ny, d, d);
	}

	void drawCrumbs() {  
	  stroke(100);
	  for (int i=0; i<CRUMB_SZ; i++) {
		point((float)crumbs[i][X], (float)crumbs[i][Y]);
	  }
	}


	void drawWayPoints() {
	  fill(0, 0, 250);
	  for (int i=0; i<NUM_WP; i++) {
		stroke(0);
		float x = calcDrawX(way_pts[i][0]);
		float y = calcDrawY(way_pts[i][1]);
		if (i==cur_way_pt) {
		  float d = calcDraw(2*WP_DIST);
		  noFill();
		  ellipse(x, y, d, d);
		  fill(0, 0, 250);
		}
		ellipse(x,y, 5, 5);
	  }
	}

	float calcDrawV(double d) {
	  float v = (float)(d*SCALE_V);
	  return v;
	}

	float calcDraw(double d) {
	  float v = (float)(d*SCALE_P);
	  return v;
	}

	float calcDrawX(double x) {
	  float dx = X_OFF + calcDraw(x);
	  return dx;
	}

	float calcDrawY(double y) {
	  float dy = Y_OFF + calcDraw(y);
	  return dy;
	}

	double calcDist(double x, double y) {
	  double d = sqrt((float)(x*x + y*y));
	  return d;
	}

	void keyPressed() {
	  switch (key) {
		case ' ':
		  initSim();
		  break;
		case 'p':
		  isStart = !isStart;
		  break;
	  }
	}
