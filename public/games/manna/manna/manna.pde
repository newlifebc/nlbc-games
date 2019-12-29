import kinect4WinSDK.Kinect;
import kinect4WinSDK.SkeletonData;
import fisica.*;
import processing.sound.*;
SoundFile _soundBite;

Kinect _kinect;
ArrayList <SkeletonData> _bodies;

int _w3 = 1920;
int _h3 = 1200;
int _w2 = 1280;
int _h2 = 960;
int _w = 640;
int _h =480;


FWorld _world;

int _size = 100; //compute at setup
//by default 20 pixels = 1 meter

PImage[] _basketImages = new PImage[2];
PImage[] _flakeImages = new PImage[5];
PImage[] _otherImages = new PImage[4];
PImage _background = new PImage();
int _flakeImageCount = 5;
int _otherImageCount = 4;

FBox _basket;
float[] _lastHand = new float[2];

int _mannaTarget = 10;
int _mannaCollected = 0;
int _otherCollected = 0;
int _score = 0;
int _mannaExactCollectedScore = 0;

int _lastMillis = 0;
int _currMillis = 0;
int _deltaMillis = 0;
int _timerMillis = 0;
int _timeDurationMillis = 60000;


void loadAssets(){
  _basketImages[0] = loadImage("basket_all.png");
  _basketImages[1] = loadImage("basket_front.png");
  _flakeImages[0] = loadImage("flake_0.png");
  _flakeImages[1] = loadImage("flake_1.png");
  _flakeImages[2] = loadImage("flake_2.png");
  _flakeImages[3] = loadImage("flake_3.png");
  _flakeImages[4] = loadImage("flake_4.png");
  _otherImages[0] = loadImage("mango_0.png");
  _otherImages[1] = loadImage("mango_1.png");
  _otherImages[2] = loadImage("quail_0.png");
  _otherImages[3] = loadImage("mayo_0.png");
  _background = loadImage("desert.jpg");
}


String _collectString = "";

void restart(){
  _mannaTarget = 10;
  _mannaCollected = 0;
  _otherCollected = 0;
  _score = 0;
  _mannaExactCollectedScore = 0;
  _timerMillis = 0;
  int day = int(random(7));
  switch(day){
    case 0:
    _collectString = "Today is Monday. Only collect "+_mannaTarget+" manna.";
    break;
    case 1:
    _collectString = "Today is Tuesday. Only collect "+_mannaTarget+" manna.";
    break;
    case 2:
    _collectString = "Today is Wednesday. Only collect "+_mannaTarget+" manna.";
    break;
    case 3:
    _collectString = "Today is Thursday. Only collect "+_mannaTarget+" manna.";
    break;
    case 4:
    _collectString = "Today is Friday. Only collect "+_mannaTarget+" manna.";
    break;
    case 5:
    _mannaTarget = 20;
    _collectString = "Today is Saturday. Collect "+_mannaTarget+" manna!";
    break;
    case 6:
    _mannaTarget = 0;
    _collectString = "Today is Sunday. Don't collect any manna!";
    break;
  }
  _doPlay = false;
}

void setup()
{
  //size(1920, 1200);
  fullScreen();
  background(0);
  
  //_soundfile = new SoundFile(this, "TheForestAwakes.mp3");
  //_soundfile.loop();
  _soundBite = new SoundFile(this, "172139__paulmorek__nom-d-02.wav");
  
  _kinect = new Kinect(this);
  smooth();
  _bodies = new ArrayList<SkeletonData>();
  _size = int(width/20);
  
  
  
  
  loadAssets();
  
  Fisica.init(this);
  _world = new FWorld();
  //_world.setScale(100);
  _world.setGravity(0,1000);
  _world.setEdges();
  _world.remove(_world.top);
  _world.remove(_world.bottom);
  _world.setGrabbable(true);
  
  _size = int(width/4);
  _basket = new FBox(_size,_size/5);
  _basket.setPosition(width/2, height/2);
  _basket.attachImage(_basketImages[0]);
  _basket.setStatic(true);
  _basket.setRotatable(false);
  _basket.setGrabbable(true);
  _basket.setName("basket");
  _world.add(_basket);
  
  restart();
}


void drawScores(){
  int mannaDiff = _mannaCollected-_mannaTarget;
  int mannaOver = 0;
  if(mannaDiff<0){
    mannaOver = 0;
  }
  int mannaUnder = _mannaCollected;
  if(mannaOver>0){
    mannaUnder = _mannaTarget;
  }
  if(mannaDiff==0){
    _mannaExactCollectedScore += _deltaMillis;
  }
  
  _score = mannaUnder*10 - mannaOver*2 - _otherCollected*2 + _mannaExactCollectedScore/1000;
  
  
  textAlign(CENTER);
  textSize(_size/10);
  fill(255);
  //text("only collect "+_mannaTarget+" manna",width/2,height-_size/10);
  text(_collectString,width/2,height-_size/10);
  text("Manna",_size,_size/10);
  text("Score",width/2,_size/10);
  text("Other",width-_size,_size/10);
  text(_score,width/2,_size/5);
  
  if(_mannaCollected>_mannaTarget){
    fill(255,255,0);
  }else{
    fill(255);
  }
  text(_mannaCollected,_size,_size/5);
  
  if(_otherCollected>0){
    fill(255,255,0);
  }else{
    fill(255);
  }
  text(_otherCollected,width-_size,_size/5); 
}


void updateTimer(){
  _currMillis = millis();
  if(_doPlay){
    _deltaMillis = _currMillis-_lastMillis;
    _timerMillis += _deltaMillis;
  }
  _lastMillis = _currMillis;
}

void drawTimer(){
  float timer = (_timeDurationMillis-_timerMillis)/1000.0;
  textAlign(RIGHT);
  textSize(_size/5);
  if(timer<10){
    fill(255,255,0);
  }else{
    fill(255);
  }
  text(nf(timer,0,2)+"s",width-_size/5,height-_size/5);
  if(timer<0.02){
    _doPlay = false;
  }
}


void tossFood(int isManna){
  FCircle fc = new FCircle(_size/2);
  
  int x = _size + (int)random(width-_size*2);
  int y = 0 - _size;
  
  float imp = (random(_size*2)-_size)*100.0;
  
  if(isManna>0){
    fc.setName("manna");
    fc.attachImage(_flakeImages[int(random(_flakeImageCount))]);
  }else{
    fc.setName("other");
    fc.attachImage(_otherImages[int(random(_otherImageCount))]);
  }
  
  fc.setPosition(x,y);
  fc.setStatic(false);
  fc.setGrabbable(false);
  fc.addTorque(random(-PI/6,PI/6));
  
  _world.add(fc);
  fc.addImpulse(imp*100.0,0);
  
}


void contactStarted(FContact contact) {
  if(contact.contains("basket")){
    if(contact.contains("manna")){
      _mannaCollected++;
      _world.remove(contact.getBody2());
    }
    if(contact.contains("other")){
      _otherCollected++;
      _world.remove(contact.getBody2());
    }
    _soundBite.play();
  }
}

int _lastTossMillis = 0;
int _tossDurationMillis = 1000;
boolean _doPlay = true;

void draw()
{
  background(0);
  image(_background,0,0);
  image(_background,_background.width,0);
    
  drawScores();
  updateTimer();
  drawTimer();
  
  //image(kinect.GetImage(), w, 0, w, h);
  //image(kinect.GetDepth(), w, h, w, h);
  //image(kinect.GetMask(), 0, h, w, h);
  //for (int i=0; i<_bodies.size (); i++) 
  //{
  //  drawSkeleton(_bodies.get(i));
  //  drawPosition(_bodies.get(i));
  //}
  
  if(_bodies.size()>0){
    SkeletonData s = _bodies.get(0);
    //check right hand/wrist
    if (s.skeletonPositionTrackingState[Kinect.NUI_SKELETON_POSITION_WRIST_RIGHT] != Kinect.NUI_SKELETON_POSITION_NOT_TRACKED){
      _lastHand[0] = (s.skeletonPositions[Kinect.NUI_SKELETON_POSITION_WRIST_RIGHT].x*width);
      _lastHand[1] = (s.skeletonPositions[Kinect.NUI_SKELETON_POSITION_WRIST_RIGHT].y*height);
      if(_lastHand[0]<0){_lastHand[0] = 0;}
      if(_lastHand[0]>(width)){_lastHand[0] = width;}
      _basket.setPosition(_lastHand[0], _lastHand[1]);
    }else{
      //check left hand/wrist instead
      if (s.skeletonPositionTrackingState[Kinect.NUI_SKELETON_POSITION_WRIST_LEFT] != Kinect.NUI_SKELETON_POSITION_NOT_TRACKED){
        _lastHand[0] = (s.skeletonPositions[Kinect.NUI_SKELETON_POSITION_WRIST_LEFT].x*width);
        _lastHand[1] = (s.skeletonPositions[Kinect.NUI_SKELETON_POSITION_WRIST_LEFT].y*height);
        _basket.setPosition(_lastHand[0], _lastHand[1]);
      }
    }
  }
  
  
  if(_doPlay){
    _currMillis = millis();
    if(_currMillis - _lastTossMillis > _tossDurationMillis){
      tossFood(int(random(2)));
      _lastTossMillis = _currMillis;
      _tossDurationMillis = 250+(int)random(1500);
    }
  }
  
  if(_doPlay){
    _world.step();
  }
  _world.draw();
  //_world.drawDebug();
}





















void drawPosition(SkeletonData _s) 
{
  noStroke();
  fill(0, 100, 255);
  String s1 = str(_s.dwTrackingID);
  text(s1, _s.position.x*width/2, _s.position.y*height/2);
}

void drawSkeleton(SkeletonData _s) 
{
  // Body
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_HEAD, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_CENTER);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_CENTER, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_CENTER, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_CENTER, 
  Kinect.NUI_SKELETON_POSITION_SPINE);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT, 
  Kinect.NUI_SKELETON_POSITION_SPINE);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT, 
  Kinect.NUI_SKELETON_POSITION_SPINE);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SPINE, 
  Kinect.NUI_SKELETON_POSITION_HIP_CENTER);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_HIP_CENTER, 
  Kinect.NUI_SKELETON_POSITION_HIP_LEFT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_HIP_CENTER, 
  Kinect.NUI_SKELETON_POSITION_HIP_RIGHT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_HIP_LEFT, 
  Kinect.NUI_SKELETON_POSITION_HIP_RIGHT);

  // Left Arm
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT, 
  Kinect.NUI_SKELETON_POSITION_ELBOW_LEFT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_ELBOW_LEFT, 
  Kinect.NUI_SKELETON_POSITION_WRIST_LEFT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_WRIST_LEFT, 
  Kinect.NUI_SKELETON_POSITION_HAND_LEFT);

  // Right Arm
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT, 
  Kinect.NUI_SKELETON_POSITION_ELBOW_RIGHT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_ELBOW_RIGHT, 
  Kinect.NUI_SKELETON_POSITION_WRIST_RIGHT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_WRIST_RIGHT, 
  Kinect.NUI_SKELETON_POSITION_HAND_RIGHT);

  // Left Leg
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_HIP_LEFT, 
  Kinect.NUI_SKELETON_POSITION_KNEE_LEFT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_KNEE_LEFT, 
  Kinect.NUI_SKELETON_POSITION_ANKLE_LEFT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_ANKLE_LEFT, 
  Kinect.NUI_SKELETON_POSITION_FOOT_LEFT);

  // Right Leg
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_HIP_RIGHT, 
  Kinect.NUI_SKELETON_POSITION_KNEE_RIGHT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_KNEE_RIGHT, 
  Kinect.NUI_SKELETON_POSITION_ANKLE_RIGHT);
  DrawBone(_s, 
  Kinect.NUI_SKELETON_POSITION_ANKLE_RIGHT, 
  Kinect.NUI_SKELETON_POSITION_FOOT_RIGHT);
}

void DrawBone(SkeletonData _s, int _j1, int _j2) 
{
  noFill();
  stroke(255, 255, 0);
  if (_s.skeletonPositionTrackingState[_j1] != Kinect.NUI_SKELETON_POSITION_NOT_TRACKED &&
    _s.skeletonPositionTrackingState[_j2] != Kinect.NUI_SKELETON_POSITION_NOT_TRACKED) {
    line(_s.skeletonPositions[_j1].x*width/2, 
    _s.skeletonPositions[_j1].y*height/2, 
    _s.skeletonPositions[_j2].x*width/2, 
    _s.skeletonPositions[_j2].y*height/2);
  }
}

void appearEvent(SkeletonData _s) 
{
  if (_s.trackingState == Kinect.NUI_SKELETON_NOT_TRACKED) 
  {
    return;
  }
  synchronized(_bodies) {
    _bodies.add(_s);
  }
}

void disappearEvent(SkeletonData _s) 
{
  synchronized(_bodies) {
    for (int i=_bodies.size ()-1; i>=0; i--) 
    {
      if (_s.dwTrackingID == _bodies.get(i).dwTrackingID) 
      {
        _bodies.remove(i);
      }
    }
  }
}

void moveEvent(SkeletonData _b, SkeletonData _a) 
{
  if (_a.trackingState == Kinect.NUI_SKELETON_NOT_TRACKED) 
  {
    return;
  }
  synchronized(_bodies) {
    for (int i=_bodies.size ()-1; i>=0; i--) 
    {
      if (_b.dwTrackingID == _bodies.get(i).dwTrackingID) 
      {
        _bodies.get(i).copy(_a);
        break;
      }
    }
  }
}




void keyPressed() {
  final int k = keyCode;

  if (k == 'P')
  _doPlay = !_doPlay;
  
  if (k == 'R')
    restart();
}