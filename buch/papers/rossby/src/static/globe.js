let r = 0;

let thetaMaxSlider, phiMaxSlider;
let densitySlider;
let thetaMax, phiMax;
let density = 100;

function preload() {
  // Load an Earth texture with oceanic contours (replace with a better one if needed)
  earthTexture = loadImage('/static/images/world.jpg');
}

function setup(){
  createCanvas(windowWidth, windowHeight, WEBGL);//size(600, 400);
  colorMode(HSB);
  stroke(321, 38, 80);
  strokeWeight(2);
  noFill();
  angleMode(RADIANS)
  r = width/4;

}

function draw(){
  background(230, 50, 15);
  orbitControl(4, 4);//Mouse control

  for(let phi = 0; phi < TWO_PI; phi += TWO_PI/density){
    for(let theta = 0; theta < TWO_PI; theta += TWO_PI/density){
      let x = r * cos(phi);
      let y = r * sin(phi) * sin(theta);
      let z = r * sin(phi) * cos(theta);
      colorMode(HSB);
      stroke(321, 38, 80);
      strokeWeight(5);
      point(x, y, z);
    }
  }
  push();
  noStroke();
  fill(255,255,255,100);
  texture(earthTexture);
  sphere(r);

  pop();


  let mappedDensity = int(map(density, 13, 72, 1, 60));
}