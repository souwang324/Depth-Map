# generateDepthmap.py

import vtk
import numpy as np
import cv2
import time
import os

def get_program_parameters():
    import argparse
    description = 'Read a .stl file.'
    epilogue = ''''''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('filename', help='42400-IDGH.stl')
    args = parser.parse_args()
    return args.filename

def ReadPolyData(file_name):
    import os
    path, extension = os.path.splitext(file_name)
    extension = extension.lower()
    if extension == '.ply':
        reader = vtk.vtkPLYReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.vtp':
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.obj':
        reader = vtk.vtkOBJReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.stl':
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.vtk':
        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == '.g':
        reader = vtk.vtkBYUReader()
        reader.SetGeometryFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    else:
        # Return a sphere if the extension is unknown.
        source = vtk.vtkSphereSource()
        source.Update()
        poly_data = source.GetOutput()
    return poly_data

def main():
    filepath_o = r'../Data'
    if not os.path.exists(filepath_o):
        os.makedirs(filepath_o)
    # Load the mesh
    filename = get_program_parameters()
    polyData = ReadPolyData(filename)

    # Create a mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    # Create an actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)  # White background

    # Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.SetOffScreenRendering(1)
    render_window.AddRenderer(renderer)

    # Create a render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filevideo = filepath_o + '/out.mp4'
    out = cv2.VideoWriter(filevideo, fourcc, 20.0, render_window.GetSize(), isColor=False)
    # Set camera position
    for n in range(0, 6 * 60, 10):
        time.sleep(0.05)
        renderer.GetActiveCamera().Azimuth(10)
        camera = renderer.GetActiveCamera()
        #camera.SetPosition(0, 0, 10)  # Adjust as needed
        #camera.SetFocalPoint(0, 0, 0)  # Adjust as needed
        renderer.ResetCamera()
        # Render the scene
        render_window.Render()

        # Get the depth buffer
        z_buffer = vtk.vtkFloatArray()
        render_window.GetZbufferData(0, 0, render_window.GetSize()[0] - 1, render_window.GetSize()[1] - 1, z_buffer)

        # Convert the depth buffer to a numpy array
        width, height = render_window.GetSize()
        depth_array = np.zeros((height, width), dtype=np.float32)
        for i in range(height):
            for j in range(width):
                depth_array[i, j] = z_buffer.GetValue(i * width + j)

        # Normalize the depth map
        depth_array = cv2.normalize(depth_array, None, 0, 1, cv2.NORM_MINMAX)

        # Save the depth map as an image
        depth_image = (depth_array * 255).astype(np.uint8)
        depth_imageR = np.bitwise_not(depth_image)

        if n == 0:
            out = cv2.VideoWriter(filevideo, fourcc, 20.0, (width, height), isColor=False)
        out.write(depth_imageR)
        filename_o =filepath_o + f'/42400-IDGH{n}Depth.png'
        if cv2.imwrite(filename_o, depth_imageR):
            print(filename_o + ' saved ')
        else:
            print(filename_o + ' failed to save')




    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()