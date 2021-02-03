
let modules = [];
let objectsSelected = false;

let pose;
let hands;

let socket;

function setup() {
  createCanvas(windowWidth, windowHeight);

  socket = io.connect('http://0.0.0.0:5000');

  let clock = new p5(Clock);
  clock.set(width - 200, 0, 200, 200);
  modules.push(clock);

  let bubble = new p5(HeartBubble);
  bubble.set(0, 0, width, height);
  modules.push(bubble);

  let multiplications = new p5(Multiplications);
  multiplications.set(0, 0, 150, 150);
  modules.push(multiplications);

  pose = new p5(Pose);
  pose.set(0, 0, width, height);
  modules.push(pose);

  hands = new p5(Hands);
  hands.set(0, 0, width, height);
  modules.push(hands);

  frameRate(30);
}

function draw() {
  background(0);
  modules.forEach(m => {
    if(m.activated){
      m.show();
      if(m.latched){
        m.setPosition(mouseX - m.OffsetX, mouseY - m.OffsetY);
      }
    }
  });
}



function keyPressed(){
  if(key == "c"){
    modules.forEach(m => {
      m.clearSketch();
    });
  }

  if(key == "p"){
    modules.forEach(m => {
      m.activated = false;
      m.selfCanvas.hide();
    });
    pose.activated = true;
    pose.selfCanvas.show();
  }

  if(key == "h"){
    modules.forEach(m => {
      m.activated = false;
      m.selfCanvas.hide();
    });
    hands.activated = true;
    hands.selfCanvas.show();
  }

  if(key == "b"){
    modules.forEach(m => {
      m.activated = false;
      m.selfCanvas.hide();
    });
    pose.activated = true;
    pose.selfCanvas.show();
    hands.activated = true;
    hands.selfCanvas.show();
  }

  if(key == "a"){
    modules.forEach(m => {
      m.activated = true;
      m.selfCanvas.show();
    });
  }
}

function mousePressed(){
  let selected = false;
  let objectSelected = false;
  modules.forEach(m => {
    if(m.movable && mouseX > m.x && mouseY > m.y && mouseX < m.x + m.width && mouseY < m.y + m.height){
      selected = true;
      if(!objectsSelected){
        m.latched = true;
        objectSelected = true;
        m.OffsetX = mouseX - m.x;
        m.OffsetY = mouseY - m.y;
      }
      else {
        m.latched = false;
      }
    }
  });

  objectsSelected = objectSelected;

  if(!selected){
    modules.forEach(m => {
      if(!m.movable && m.clickable){
        m.onClicked(mouseX, mouseY);
      }
    });
  }
}
