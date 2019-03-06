import plotly as py
import plotly.graph_objs as go
import numpy as np
import math

def get_constants():
    RHO = 28
    SIGMA = 10
    BETA = 8/3
    return RHO,SIGMA ,BETA

def get_critical_points():
    RHO, _, BETA = get_constants()
    x1 = math.sqrt(BETA*(RHO-1))
    y1 = math.sqrt(BETA*(RHO-1))
    z1 = RHO-1
    point_1 = np.array([x1,y1,z1])

    x2 = -x1
    y2 = -y1
    z2 = z1
    point_2 = np.array([x2, y2, z2])
    return point_1, point_2

def init_pyplot_figure():
    critical_point1, critical_point2 = get_critical_points()
    figure = {"layout":{'xaxis': {'range': [0, 5], 'autorange': False},
              'yaxis': {'range': [0, 5], 'autorange': False},
              "scene":{"camera":dict(up=dict(x=0, y=0, z=0.5),center=dict(x=0, y=0, z=0),eye=dict(x=1.25, y=0, z=1.25))},
              'title': 'Lorenz attractor'},
              "data":[dict(type="scatter3d", x=[0], y=[0], z=[0], marker = dict(color="rgb(0,255,0)")),
                      dict(type="scatter3d", x=[0], y=[0], z=[0], marker = dict(color="rgb(0,255,0)")),
                      dict(type="scatter3d", name="critical point 1", marker = dict(color="rgb(255,0,0)"),
                           x=[critical_point1[0]], y=[critical_point1[1]], z=[critical_point1[2]]),
                      dict(type="scatter3d", name="critical point 2", marker = dict(color="rgb(255,0,0)") ,
                           x=[critical_point2[0]], y=[critical_point2[1]], z=[critical_point2[2]])]}
    return figure


def next_particle_position(old_particle_position, dt):
    RHO, SIGMA, BETA =  get_constants()
    old_x, old_y, old_z = old_particle_position

    new_particle_x = old_x+SIGMA*(old_y-old_x)*dt
    new_particle_y = old_y+(old_x*(RHO-old_z)-old_y)*dt
    new_particle_z = old_z+(old_x*old_y-BETA*old_z)*dt

    new_particle_position = np.array((new_particle_x,
                                      new_particle_y,
                                      new_particle_z))
    return new_particle_position



def make_step(nth_frame, plot_figure, particle_art, particle_data):
    DT = 0.01
    old_particle_position = particle_data.old_particle_position
    for i in range(1000):
        new_particle_position = next_particle_point(old_particle_position, DT)
    update_particle_art(particle_art, new_particle_position)
    draw_art_list = [particle_art]
    #optimizing by not plottinng a line in every 5 steps
    if(nth_frame%5 == 0):
        path_line = render_particle_path(plot_figure, old_particle_position, new_particle_position)
        draw_art_list = [particle_art, path_line]
    particle_data.old_particle_position = new_particle_position
        #FuncAnimation will plot the artist that are returend in the list
    return draw_art_list

def generate_particle_path(initial_position):
    new_particle_position = np.array(initial_position)
    particle_path = [new_particle_position]
    dt = 0.01
    plot_every_nth_step = 5
    for i in range(1000):
        new_particle_position = next_particle_position(new_particle_position,dt)
        #for optimiziation
        if(i % plot_every_nth_step ==0):
            particle_path.append(new_particle_position)
    return particle_path

def generate_frames(particle_path):
    frames = []
    x_data = []
    y_data = []
    z_data = []
    for particle_position in particle_path:
        x_data.append(particle_position[0])
        y_data.append(particle_position[1])
        z_data.append(particle_position[2])
        trace = {'type': 'scatter3d',
            "x":x_data, "y":y_data, "z":z_data,
            "mode":'lines'}
        trace = go.Scatter3d(x=x_data, y=y_data,z=z_data, mode="lines", name="particle trajectory")
        particle = {'type': 'scatter3d',
            "x":[x_data[-1]], "y":[y_data[-1]], "z":[z_data[-1]],
            "mode":'markers',
            "name":"particle"}
        frame = dict(data=[trace, particle])
        frames.append(frame)

    return frames

def concatenate_frames(frame1, frame2):
    concatenated_frames = []
    for frame_index in range(len(frame1)):
        data1 = frame1[frame_index]["data"]
        data2 = frame2[frame_index]["data"]
        new_frame = dict(data=data1+data2)
        concatenated_frames.append(new_frame)
    return concatenated_frames
        

if (__name__ == "__main__"):
    figure = init_pyplot_figure()
    initial_particle1 = [1,2,3]
    initial_particle2 = [1,2,3.1]
    particle_path1 = generate_particle_path(initial_particle1)
    particle_path2 = generate_particle_path(initial_particle2)
    frames1 = generate_frames(particle_path1)
    frames2 = generate_frames(particle_path2)
    concatenated_frames = concatenate_frames(frames1, frames2)
    figure["frames"] = concatenated_frames
    py.offline.plot(figure)

    

