import numpy as np
from perception import check_rocks, to_polar_coords, pix_to_world


# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):
    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # print some info for debugging
        print("Current mode: ", Rover.mode)
        print("throttle_count:", Rover.throttle_count)

        make_decision(Rover)

    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set[0]
        Rover.steer = 0
        Rover.brake = 0

    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True

    return Rover
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_hard
                Rover.steer = 0
                Rover.mode = 'pickup'
        elif Rover.mode == 'pickup':
            if Rover.vel > 0.2:
            # Get new steer value
            new_steer = get_navi_steer(Rover)
                Rover.throttle = 0
                Rover.brake = Rover.brake_hard
                Rover.steer = 0
            # If in a state where want to pickup a rock send pickup command
            if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
                Rover.send_pickup = True  
                Rover.mode = 'forward'
            elif not Rover.near_sample:
                Rover.mode = 'forward'
        elif Rover.mode == 'decelerate':
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            if len(Rover.nav_angles) < Rover.stop_forward:
                # Set mode to "stop" and hit the brakes!
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_hard
                Rover.steer = 0
                Rover.mode = 'stop'
            elif len(Rover.nav_angles) >= Rover.go_forward:
                # Set throttle back to stored value
                Rover.throttle = Rover.throttle_set
                # Release the brake
                Rover.brake = 0
                Rover.mode = 'forward'
        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_hard
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    #last_nav_angles_len = len(Rover.angles)
                    Rover.steer = 15 # Could be more clever here about which way to turn
                    #if len(Rover.angles) < last_nav_angles_len: # wrong direction
                    #    Rover.steer = -15
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
              
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

# Get next steer
def get_navi_steer(Rover):
    if Rover.is_going_home:
        # get home pos
        home = Rover.home
        # get current rover pos
        pos = Rover.pos
        # convert them into world coords
        home_world_x, home_world_y = pix_to_world(home[0], home[1], pos[0], pos[1], Rover.yaw, Rover.worldmap.shape[0],
                                                  10)
        home_world_dist, home_world_angle = to_polar_coords(home_world_x, home_world_y)

        mean_angle = np.mean(Rover.nav_angles)

        # Steer toward home
        if mean_angle > home_world_angle:
            steer = -10
        else:
            steer = +10
    else:
        # Set steering to average angle clipped to the range +/- 15
        steer = np.mean(Rover.nav_angles * 180 / np.pi) + 14.9  # lean towards left side wall

    return np.clip(steer, -15, 15)
