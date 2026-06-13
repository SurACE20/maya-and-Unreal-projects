//Maya ASCII 2024
createNode transform -n "room";
createNode mesh -n "floorShape" -p "room";
createNode transform -n "floor";
setAttr "floor.translateY" 0;
createNode polyPlane -n "polyPlane1";
createNode transform -n "crate";
createNode polyCube -n "polyCube1";
createNode camera -n "camera1";
setAttr "camera1.translateZ" 10;
setAttr "camera1.translateY" 5;
