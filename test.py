for ( var i:int = 4; i < points.length; i++ ){
    v = points[ i ];
    #checks the point's visibility from all faces
    visibleFaces.length = 0;
	for each( face in validFaces ){	
		if ( face.isVisible( v ) ){
						visibleFaces.push( face ); 
		}
	}
				
    #the vertex is not visible : it is inside the convex hull, keep on
	if ( visibleFaces.length == 0 ){
					continue;
	}
				
    #the vertex is outside the convex hull
	#delete all visible faces from the valid List
	for each ( face in visibleFaces ){
					validFaces.splice( validFaces.indexOf( face ), 1 );
	}
				
	#special case : only one face is visible
	#it's ok to create 3 faces directly for they won't enclose any other point
	if ( visibleFaces.length == 1 ){
					face = visibleFaces[ 0 ];
					validFaces.push( new Face( i, face.i0, face.i1 ) );
					validFaces.push( new Face( i, face.i1, face.i2 ) );
					validFaces.push( new Face( i, face.i2, face.i0 ) );
					continue;
	}
				
	#creates all possible new faces from the visibleFaces
	tmpFaces.length = 0;
	for each( face in visibleFaces ){
					tmpFaces.push( new Face( i, face.i0, face.i1 ) );
					tmpFaces.push( new Face( i, face.i1, face.i2 ) );
					tmpFaces.push( new Face( i, face.i2, face.i0 ) );
	}
	var other:Face;
	for each( face in tmpFaces ){
		#search if there is a point in front of the face : 
		#this means the face doesn't belong to the convex hull
		search : for each( other in tmpFaces ){
				if ( face != other ){
					if ( face.isVisible( other.centroid ) ){
								face = null;
								break search;
							}
						}
					}
					#the face has no point in front of it
					if ( face != null ) validFaces.push( face );
				}
}