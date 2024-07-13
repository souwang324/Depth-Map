

# fromMeshToDepthmap2.py

import vtk
import os
import numpy as np

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
    filename = get_program_parameters()
    polyData = ReadPolyData(filename)
    renderer = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    interactor = vtk.vtkRenderWindowInteractor()
    colors = vtk.vtkNamedColors()

    # Build visualization enviroment
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Tan"))
    actor.SetOrientation(0, 0, 0)
    #actor.RotateX(60)
    actor.RotateY(-60)

    # camera = vtk.vtkCamera()
    # camera.SetPosition(0, 0, 100)
    # camera.SetFocalPoint(0, 0, 0)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d("SlateGray"))
    #renderer.SetActiveCamera(camera)

    renWin.AddRenderer(renderer)
    renWin.SetWindowName("WindowModifiedEvent")

    interactor.SetRenderWindow(renWin)
    renWin.Render()

    filter = vtk.vtkWindowToImageFilter()
    filter.SetInput(renWin)
    filter.SetScale(2)
    filter.SetInputBufferTypeToZBuffer()
    filter.Update()

    # image = filter.GetOutput()
    # bounds = 6 * [0.0]
    # image.GetBounds(bounds)
    #print(bounds)
    scale = vtk.vtkImageShiftScale()
    scale.SetOutputScalarTypeToUnsignedChar()
    scale.SetInputConnection(filter.GetOutputPort())
    scale.SetShift(0)
    scale.SetScale(-255)
    # scale.SetShift(-1.0 * bounds[0])
    # oldRange = bounds[1] - bounds[0]
    # newRange = 255
    #
    # scale.SetScale(newRange / oldRange)
    scale.Update()



    imageWriter = vtk.vtkBMPWriter()
    imageWriter.SetFileName("depthmap1.bmp")
    imageWriter.SetInputConnection(scale.GetOutputPort())
    imageWriter.Write()

    interactor.Start()


if __name__ == '__main__':
    main()