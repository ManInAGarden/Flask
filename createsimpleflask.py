from build123d import *
from ocp_vscode import *
from bd_warehouse.thread import MetricTrapezoidalThread, PlasticBottleThread


#parameters
diameter = 60*MM
lid_thickn = 2*MM
thread_height = 18*MM
usable_height = 70*MM
#wall_width = 5*MM
botthickn = 5*MM
topinnerdia = 55*MM
slackn = 0.3*MM
hborderw = 7*MM # width of the top border (on the bolt)
handlew = 5*MM # width of the handle which is sunk into the bolt top

#calculated, do not change

flask_height = thread_height + lid_thickn + usable_height
flask_radius = diameter/2
bolttopdia = topinnerdia - 2*slackn
wall_width = diameter - topinnerdia
handled = thread_height/2
thread_interfear = 1.0 #overlap of thread windings to bolt or nut

hlp_ali = (Align.CENTER,Align.CENTER, Align.MIN)
cyl = Plane.XY  * Cylinder(flask_radius, flask_height, align=hlp_ali)
cyl -= Plane.XY * Pos(0,0,botthickn) * Cylinder(topinnerdia/2, flask_height+lid_thickn, align=hlp_ali)
inthr = Plane.XY * Pos(0,0, usable_height) * MetricTrapezoidalThread(size="55x9",
                                                                     length=thread_height, 
                                                                     external=False, 
                                                                     end_finishes=("fade", "fade"),
                                                                     align=hlp_ali)
cyl = chamfer(cyl.edges().group_by(Axis.Z)[1], length=2*MM)
cyl = chamfer(cyl.edges().group_by(Axis.Z)[0], length=2*MM)

wallsk = Plane.XZ * Pos(-0.2*(diameter-wall_width)/2,usable_height*0.8/2) * make_face(Rectangle(1.2*MM, usable_height*0.9))
wall = extrude(wallsk, until=Until.LAST, target=cyl)
wall += extrude(wallsk, until=Until.FIRST, target=cyl)
cyl += wall


boltthr = Plane.XY * Pos(0,0, usable_height) * MetricTrapezoidalThread(size="55x9",
                                                                     length=thread_height, 
                                                                     external=True, 
                                                                     end_finishes=("fade", "fade"),
                                                                     align=hlp_ali)
bolt = Part() + Plane.XY * Pos(0,0, usable_height) * Cylinder(boltthr.root_radius, thread_height, align=hlp_ali)
bolt += Plane.XY * Pos(0,0,usable_height + thread_height) * Cylinder(bolttopdia/2*MM, lid_thickn)

bolt_topf = bolt.faces().sort_by(Axis.Z).last
toppl = Plane(bolt_topf)

r=bolttopdia/2-hborderw
hsketch_u = Sketch() + SagittaArc(start_point=(-r,handlew/2),end_point=(r,handlew/2), sagitta=r-handlew/2) + Line(((-r,handlew/2),(r,handlew/2)))
hsketch_l = Sketch() + SagittaArc(start_point=(r,-handlew/2),end_point=(-r,-handlew/2), sagitta=r-handlew/2) + Line(((r,-handlew/2),(-r,-handlew/2)))
cutoutf_u = make_face(hsketch_u)
cutoutf_l = make_face(hsketch_l)
cutout = extrude(cutoutf_u, -handled) + extrude(cutoutf_l, -handled)

cyl += inthr
bolt -= toppl * cutout
bolt = chamfer(bolt.edges().group_by(Axis.Z)[0], 2.0)
bolt += boltthr

export_stl(bolt.solid(), "./stl/lid.stl")
export_stl(cyl.solid(), "./stl/body.stl")

show_all()