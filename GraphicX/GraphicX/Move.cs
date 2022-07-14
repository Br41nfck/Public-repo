using System.Drawing;
using System.Windows.Forms;

namespace GraphicX
{
    public partial class Main : Form
    {
        private Point previousLocation;

        private void MoveGraph(Point loc)
        {
            // changes location of picturebox_graph based on (mouse) location

            Point location = pictureBox_graph.Location;
            location.Offset(loc.X - previousLocation.X, loc.Y - previousLocation.Y);
            LocationCorrection(ref location);
            pictureBox_graph.Location = location;
        }

        private void LocationCorrection(ref Point location)
        {
            // corrects the location of pictureBox_graph if it gets inside the boudaries of picturebox_container
            if (location.X > 0)
                location.X = 0;
            if (location.Y > 0)
                location.Y = 0;
            if (location.X + pictureBox_graph.Width < pictureBox_container.Width)
                location.X = pictureBox_container.Width - pictureBox_graph.Width;
            if (location.Y + pictureBox_graph.Height < pictureBox_container.Height)
                location.Y = pictureBox_container.Height - pictureBox_graph.Height;
        }

        private bool IsMouseOutside()
        {
            // checks if mouse is outside of boundaries of picturebox_container

            Point mousePos_container = pictureBox_container.PointToClient(Control.MousePosition);
            if (mousePos_container.X < 0 || mousePos_container.X > pictureBox_container.Width || mousePos_container.Y < 0 || mousePos_container.Y > pictureBox_container.Height)
                return true;
            else
                return false;
        }
    }
}
