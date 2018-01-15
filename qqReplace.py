### trying to edit on github
### second edit 

######################################
####### replace with variable names
######################################

node = hou.selectedNodes()[0]
snippet = node.parm("snippet")
actualcode = snippet.evalAsString()
lines = actualcode.split('\n')

for line in lines:
    found = 0
    if line.startswith("qqf."):
        qq,var = line.split('.')
        newline = 'float ' + var + ' = chf("' + var + '"); // 0.5 in 0.0 to 1.0'
        found = 1
        
    if line.startswith("qqi."):
        qq,var = line.split('.')        
        newline = 'int ' + var + ' = chi("' + var + '"); // 1 in 0 to 10'
        found = 1
        
    if line.startswith("qqr."):
        qq,var = line.split('.')        
        newline = var + ' = chramp("' + var + '",' + var + '); //' + var
        found = 1

    if found:
        actualcode = actualcode.replace(line,newline,1) # only the first occurrence


snippet.set(actualcode)      

######################################
####### library without variable names
######################################


    
src = []
rep = []




src.append("qqfor")
###
rep.append('''for (int i = 0; i < count; i++)
{
    
}''')




src.append("qqif")
###
rep.append('''if (  )
{
    
}''')




src.append("qqfeach")
###
rep.append('''foreach (float read; array[])
{
    
}''')




src.append("qqpt")
###
rep.append('''point(0, "P", @ptnum);''')




src.append("qqdet")
###
rep.append('''detail(0, "name");''')




src.append("qqprim")
###
rep.append('''prim(0, "name", primnum);''')




src.append("qqsetpt")
###
rep.append('''setpointattrib(0, "name", @ptnum, value, "set");''')




src.append("qqsetprim")
###
rep.append('''setprimattrib(0, "name", @primnum, value, "set");''')




src.append("qqsetdet")
###
rep.append('''setdetailattrib(0, "name", value, "set");''')




src.append("qqrandir")
###
rep.append('''vector center = {0,0,1};
float  maxangle = radians( chf("maxangle") ); // 45 in 0 to 90
v@N = sample_direction_cone( center, maxangle, rand(@ptnum) );''')




src.append("qqrotmat")
###
rep.append('''float angle = radians( 90 );
vector axis = {0,1,0};
matrix3 m = ident();
rotate(m, angle, axis);''')




src.append("qqaddpt")
###
rep.append('''int ptnum = addpoint(0, @pos );
int primnum = addprim(0, "poly" ); //poly, polyline
int vertnum = addvertex(0, primnum, ptnum);
setpointattrib(0, "name", pt, value, "set");''')




src.append("qqrbx")
###
rep.append('''float x = getcomp( relbbox(0,@P) , 0 );''')




src.append("qqnearpts")
###
rep.append('''float maxdist = chf("maxdist"); // 1 in 0 to 2
int maxpts = chf("maxpts"); // 1 in 1 to 100
array[] = nearpoints(0, vector pt, maxdist, int maxpts);''')




src.append("qqrempt")
###
rep.append('''removepoint(0, @ptnum);''')




src.append("qqremprim")
###
rep.append('''removeprim(0, @primnum, andpoints);''')




src.append("qqvolsamp")
###
rep.append('''volumesample(0, primnum, pos);''')




src.append("qqxyzdist")
###
rep.append('''xyzdist(0, pos, int &prim, vector &uv, float maxdist);''')




src.append("qqfit")
###
rep.append('''float value;
float omin = chf("old_min"); // 0 in 0 to 1
float omax = chf("old_max"); // 1 in 0 to 1
float nmin = chf("new_min"); // 0 in 0 to 1
float nmax = chf("new_max"); // 1 in 0 to 1
fit(value, omin, omax, nmin, nmax);''')




src.append("qqsmooth")
###
rep.append('''float value;
float omin = chf("old_min"); // 0 in 0 to 1
float omax = chf("old_max"); // 1 in 0 to 1
float rolloff = chf("rolloff"); // 1 in 0 to 1
//rollof =  1
smooth(omin, omax, value, float rolloff); ''')




src.append("qqlerp")
###
rep.append('''vector from;
vector to;
float amount = 0;
vector lerp(from, to, amount);''')




src.append("qqlookat")
###
rep.append('''
vector from;
vector to;
vector up;
matrix3 mrot = lookat(from, to, up);''')




src.append("qqpc")
###
rep.append('''float radius = chf("radius"); // 1 in 0 to 2
int maxpts = chf("maxpts"); // 1 in 1 to 100
int handle = pcopen(0, "P", @P, radius, maxpts);
while(pciterate(handle))
{
    imp_pressure = pcfilter(handle, "pressure");

    pcimport(handle, "Cd", col);
    pcimport(handle, "point.distance", dist);
    pcimport(handle, "point.number", num);

    eval += imp_pressure*(1-dist/radius);
    pt_count++;
}
eval = eval/pt_count;
pcclose(handle);''')




src.append("pcfilter")
###
rep.append('''float radius = chf("radius"); // 1 in 0 to 2
int maxpts = chf("maxpts"); // 1 in 1 to 100
int handle = pcopen(0, "P", @P, radius, maxpts);
vector value = pcfilter(handle, "P");''')




src.append("qqprintf")
###
rep.append('''printf("OUT=%f; ", out); //  %s string,   %i integer''')




src.append("qqnoise")
###
rep.append('''float freqxyz = chf("frequency_xyz"); // 1 in 0 to 1
vector offset = chv("offset");
vector freq = set ( freqxyz , freqxyz , freqxyz );
float amp = chf("amplitude"); // 1 in 0 to 1
int turb = chi("turbulence"); // 3 in 0 to 5
float rough = chf("roughness"); // 0.5 in 0 to 1
float atten = chf("attenuation"); // 1 in 0 to 1
//
vector noise = onoise(@P*freq - offset, turb, rough, atten) * amp;''')



######################################
####### replace without variable names
######################################


node = hou.selectedNodes()[0]
snippet = node.parm("snippet")
actualcode = snippet.evalAsString()
index = 0
for src_item in src:
    rep_item = rep[index]
    if src_item in actualcode:
        newcode = actualcode.replace(src_item,rep_item)
        snippet.set(newcode)
    index = index+1
