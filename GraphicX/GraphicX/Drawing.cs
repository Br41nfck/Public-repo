using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace GraphicX
{
    public partial class Main : Form
    {
        const int NUM_SECTION = 20;

        int section_w = 0, section_h = 0;

        private void DrawDot()
        {
            // draws a red dot used for marking a point on the graph

            bmp_dot = new Bitmap(dot.Size.Height, dot.Size.Height);
            Graphics g = Graphics.FromImage(bmp_dot);
            g.FillEllipse(Brushes.Red, 0, 0, bmp_dot.Width / 2, bmp_dot.Height / 2);
            g.Dispose();
        }

        private void DrawGrid(double corr_factor = 1)
        {
            // calculates section sizes and draws a grid for picturebox_graph background

            int w = (int)Math.Round(pictureBox_container.Width * ZOOM_MAX);
            int h = (int)Math.Round(pictureBox_container.Height * ZOOM_MAX);
            int _section_w = (int)((Math.Round(range / NUM_SECTION, GetDecimalPlaces((decimal)xstep)) / range) * w / corr_factor);
            int _section_h = (int)((Math.Round(range / NUM_SECTION, GetDecimalPlaces((decimal)xstep)) / range) * h / corr_factor);
            if (_section_w == section_w && _section_h == section_h && corr_factor != 1) return;
            section_h = _section_h;
            section_w = _section_w;
            Bitmap bmp = new Bitmap(w, h);
            Pen pen = new Pen(Brushes.DarkGreen);
            Pen pen_axis = new Pen(Brushes.Red);
            Graphics g = Graphics.FromImage(bmp);
            Font font = new Font("Arial", (float)section_w / 4);
            int i;
            // axis
            g.DrawLine(pen_axis, new Point(w / 2 - 1, 0), new Point(w / 2 - 1, h));
            g.DrawLine(pen_axis, new Point(w / 2, 0), new Point(w / 2, h));
            g.DrawLine(pen_axis, new Point(w / 2 + 1, 0), new Point(w / 2 + 1, h));
            g.DrawLine(pen_axis, new Point(0, h / 2 - 1), new Point(w, h / 2 - 1));
            g.DrawLine(pen_axis, new Point(0, h / 2), new Point(w, h / 2));
            g.DrawLine(pen_axis, new Point(0, h / 2 + 1), new Point(w, h / 2 + 1));
            // draw zero
            g.DrawString("0", font, Brushes.Black, new Point((int)Math.Round((double)w / 2 - ((double)section_w / 4)), (int)Math.Round((double)h / 2 + (double)section_h / 4)));
            string format;
            double number;
            // left half
            for (i = w / 2 - section_w; i >= 0; i -= section_w)
            {
                g.DrawLine(pen, new Point(i, 0), new Point(i, h));
                if ((i - w / 2) % (2 * section_w) == 0)
                {
                    number = (min + (double)i / w * range);
                    format = GetFormat(number);
                    g.DrawString(number.ToString(format), font, Brushes.Black, new Point(Math.Max((int)Math.Round((double)i - ((double)section_w / 4)), 0), (int)Math.Round((double)h / 2 + (double)section_h / 4)));
                }
            }
            // upper half
            for (i = h / 2 - section_h; i >= 0; i -= section_h)
            {
                g.DrawLine(pen, new Point(0, i), new Point(w, i));
                if ((i - h / 2) % (2 * section_h) == 0)
                {
                    number = (-min - (double)i / h * range);
                    format = GetFormat(number);
                    g.DrawString(number.ToString(format), font, Brushes.Black, new Point((int)Math.Round((double)w / 2 + (double)section_w / 4), Math.Max((int)Math.Round(i - ((double)section_h / 4)), 0)));
                }
            }
            // right half
            for (i = w / 2 + section_w; i <= w; i += section_w)
            {
                g.DrawLine(pen, new Point(i, 0), new Point(i, h));
                if ((i - w / 2) % (2 * section_w) == 0)
                {
                    number = (min + (double)i / w * range);
                    format = GetFormat(number);
                    g.DrawString(number.ToString(format), font, Brushes.Black, new Point((int)Math.Round((double)i - ((double)section_w / 4)), (int)Math.Round((double)h / 2 + (double)section_h / 4)));
                }
            }
            // lower half
            for (i = h / 2 + section_h; i <= h; i += section_h)
            {
                g.DrawLine(pen, new Point(0, i), new Point(w, i));
                if ((i - h / 2) % (2 * section_h) == 0)
                {
                    number = (-min - (double)i / h * range);
                    format = GetFormat(number);
                    g.DrawString(number.ToString(format), font, Brushes.Black, new Point((int)Math.Round((double)w / 2 + (double)section_w / 4), (int)Math.Round(i - ((double)section_h / 4))));
                }
            }
            g.Dispose();
            if (bmp != null)
            {
                if (pictureBox_graph.BackgroundImage != null) pictureBox_graph.BackgroundImage.Dispose();
                pictureBox_graph.BackgroundImage = bmp;
                pictureBox_graph.BackgroundImageLayout = ImageLayout.Stretch;
            }
        }

        private void DrawGraph()
        {
            // draws 2d graph from a list of points

            Bitmap bmp = new Bitmap((int)Math.Round(pictureBox_container.Width * ZOOM_MAX), (int)Math.Round(pictureBox_container.Height * ZOOM_MAX));
            List<Point> points = values.Select(t =>
                                        new Point(
                                            (int)Math.Round(bmp.Width * (t[0] - min) / range),
                                            (int)Math.Round(bmp.Height * (1 - (t[1] - min) / range))
                                        )
                                    ).ToList();
            values_perc = points.Select(t => new double[]
                                        {
                                            (double)t.X / bmp.Width,
                                            (double)t.Y / bmp.Height
                                        }
                                    ).ToList();
            Graphics g = Graphics.FromImage(bmp);
            Pen pen = new Pen(Brushes.Black);
            g.DrawLines(pen, points.ToArray<Point>());
            g.Dispose();

            pictureBox_graph.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBox_graph.Image = bmp;
        }
    }
}
