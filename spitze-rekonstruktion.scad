///////////////////////////////////////////////


shaft_length = 20.0;
shaft_diameter = 20.0;
total_length = 104.68;
base_bore_d = 12.0;
base_bore_h = 47.11;
front_bore_d = 10.0;
diameters = [40.98, 37.96, 31.96, 25.96, 19.96, 13.96,  front_bore_d];
offsets =   [20.00, 29.70, 48.20, 65.57, 81.64, 96.17, total_length];

blank_height = 10.0;
blank_length = total_length + 20;
blank_width = 60;
support_blob_d = 6.0;
$fn=50;

// projection = true;

if(projection == undef) {
  work();
 } else {
  projection() { work(); }
}

module work() {
//tip_bore();
//rocket_tip();
//support_beam(10.0, 20);
  support_base();
}

module rocket_tip() {
  difference() {
    union() {
      tip_cone();
      tip_shaft();
    }
    //    tip_bore();
  }
}

module support_base() {
  difference() {
    translate([blank_length / 2.0, blank_width / 2.0, 0])
      cube([blank_length, blank_width, blank_height], center=true);
    rotate([0, 90, 0]) {
      % rocket_tip();
      // remove the conical part of the tip
      intersection() {
	{
	  translate([0, 0, shaft_length]) {
	    cylinder(d=diameters[0] * 2, h=total_length - shaft_length);
	  }
	}
	{
	  scale([1.3, 1.3, 1.0]) {
	    union() {
	      tip_cone();
	      tip_shaft();
	    }
	  }
	}
      }
      
    }
    // remove the shaft
    translate([shaft_length / 2.0, 0, 0]) {
      # cube([shaft_length, shaft_diameter, blank_height], center=true);
    }
  }
  for(i=[1:len(diameters) - 2]) {
    translate([offsets[i], diameters[i] / 2.0 + support_blob_d, 0]) {
      cylinder(r=support_blob_d, h=blank_height, center=true);
    }
  }
  
}

module support_beam(d, h) {
  translate([0, 0, h]) {
    rotate([45, 0, 0]) 
      cube([blank_height, d / sqrt(2.0), d / sqrt(2.0), ], center=true);
  }
  translate([0, 0, h / 2.0]) 
    cube([blank_height, d, h], center=true);
}

module tip_bore() {
  cylinder(d=base_bore_d, h=base_bore_h * 2, center=true);
  translate([0, 0, base_bore_h]) 
    cylinder(d=front_bore_d, h=(total_length - base_bore_h) * 3, center=true);
}

module tip_shaft() {
  cylinder(d=shaft_diameter, h=shaft_length);
}


module tip_cone() {
  for(i = [0:len(diameters) - 2]) {
    translate([0, 0, offsets[i]]) {
      cylinder(d1=diameters[i] , d2=diameters[i+1], h=offsets[i+1] - offsets[i]);
    }
  }
}
