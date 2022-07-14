using System;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace GraphicX
{
    public partial class Main : Form
    {
        Button dot;
        Bitmap bmp_dot;

        private void ShowCoord()
        {
            // calculates and shows coordinates based on mouse position

            Point mousePos_graph = pictureBox_graph.PointToClient(Control.MousePosition);
            labelPos.Text = Coord2String(GetCoordinates(mousePos_graph));
        }

        private void ShowCoordOnGraph()
        {
            // calculates and shows the point on graph closest to the mouse position

            Point mousePos_graph = pictureBox_graph.PointToClient(Control.MousePosition);
            Point closest_point = mousePos_graph;
            dot.Text = Coord2String(GetClosestPoint(ref closest_point));
            closest_point.Offset(-(int)Math.Round((double)dot.Size.Height / 2), -(int)Math.Round((double)dot.Size.Height / 2));
            dot.Location = closest_point;
            if (!dot.Visible)
                dot.Visible = true;
        }

        private string GetFormat(double number)
        {
            // takes the number of decimal places from xstep and returns it as format for number string representation

            int dec1 = GetDecimalPlaces((decimal)xstep);
            int dec2 = GetDecimalPlaces((decimal)number);
            return "N" + Math.Min(dec1, dec2).ToString();
        }

        private int GetDecimalPlaces(decimal number)
        {
            return BitConverter.GetBytes(decimal.GetBits(number)[3])[2];
        }

        private string Coord2String(double[] dot)
        {
            string[] format = new string[] { GetFormat(dot[0]), GetFormat(dot[1]) };
            return "   x=" + dot[0].ToString(format[0]) + " ; y=" + dot[1].ToString(format[1]);
        }

        private double[] GetCoordinates(Point position)
        {
            // calculates graph coordinates based on position in the picturebox_graph

            return new double[]
            {
                min + ((double)position.X / (double)pictureBox_graph.Width) * range,
                - min - ((double)position.Y / (double)pictureBox_graph.Height) * range
            };
        }

        private double[] GetClosestPoint(ref Point position)
        {
            // returns both coordinates on graph and Point on picturebox_graph of closest graph point to position

            Point tmp = position;
            position = (Point)values_perc.Select(t => new Point((int)Math.Round(t[0] * pictureBox_graph.Width), (int)Math.Round(t[1] * pictureBox_graph.Height)))
                                    .Select(t => new object[]
                                    {
                                            t,
                                            Math.Sqrt(Math.Pow(tmp.X - t.X, 2) + Math.Pow(tmp.Y - t.Y, 2))
                                    })
                                    .OrderBy(x => (double)x[1])
                                    .ToList()[0][0];
            return GetCoordinates(position);
        }

    }
}