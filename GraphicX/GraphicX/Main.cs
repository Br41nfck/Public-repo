using System;
using System.ComponentModel;
using System.Drawing;
using System.Threading;
using System.Windows.Forms;

namespace GraphicX
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
            this.MinimumSize = this.Size;

            this.FormClosing += Form1_FormClosing;

            pictureBox_container.BackColor = Color.Transparent;
            pictureBox_graph.BackColor = Color.Transparent;
            pictureBox_container.Controls.Add(pictureBox_graph);
            pictureBox_graph.Location = new Point(0, 0);
            pictureBox_graph.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;

            pictureBox_graph.MouseWheel += PictureBox_MouseWheel;
            pictureBox_graph.MouseDown += PictureBox_MouseDown;
            pictureBox_graph.MouseUp += PictureBox_MouseUp;

            bwCoord.DoWork += BwCoord_DoWork;
            bwCoord.ProgressChanged += BwCoord_ProgressChanged;

            bwCoord.RunWorkerAsync();

            dot = new Button();
            pictureBox_graph.Controls.Add(dot);
            dot.Visible = false;
            dot.Size = new Size(200, 20);
            dot.FlatStyle = FlatStyle.Flat;
            dot.FlatAppearance.BorderSize = 0;
            dot.ForeColor = Color.Black;
            dot.TextAlign = ContentAlignment.BottomLeft;
            DrawDot();
            dot.Image = bmp_dot;
            dot.ImageAlign = ContentAlignment.MiddleLeft;
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            bwCoord.CancelAsync();
        }

        private void ButtonPlot_Click(object sender, EventArgs e)
        {
            string formula = textBox_formula.Text;
            
            if (!GetParams())
                return;

            values = CreateOutput();

            if (values == null)
            {
                MessageBox.Show("Invalid formula!");
                return;
            }

            CalcRange();
            DrawGraph();
            DrawGrid();
        }

        private void PictureBox_MouseWheel(object sender, MouseEventArgs e)
        {
            ZoomGraph(e.Delta > 0 ? 1 : -1);
        }

        private void PictureBox_MouseUp(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                pictureBox_graph.MouseMove -= PictureBox_LeftMouseMove;
                Cursor = Cursors.Default;
            }
            else if (e.Button == MouseButtons.Right)
            {
                pictureBox_graph.MouseMove -= PictureBox_RightMouseMove;
                dot.Visible = false;
            }
        }

        private void PictureBox_MouseDown(object sender, MouseEventArgs e)
        {
            if (pictureBox_graph.Image == null)
                return;
            
            if (e.Button == MouseButtons.Left)
            {
                pictureBox_graph.MouseMove += PictureBox_LeftMouseMove;
                previousLocation = e.Location;
                Cursor = Cursors.Hand;
            }
            else if (e.Button == MouseButtons.Right)
            {
                pictureBox_graph.MouseMove += PictureBox_RightMouseMove;
            }
        }

        private void PictureBox_LeftMouseMove(object sender, MouseEventArgs e)
        {
            MoveGraph(e.Location);
        }

        private void PictureBox_RightMouseMove(object sender, MouseEventArgs e)
        {
            if (IsMouseOutside())
                return;
           
            ShowCoordOnGraph();
        }

        private void BwCoord_DoWork(object sender, DoWorkEventArgs e)
        {
            while (true)
            {
                Thread.Sleep(1);
                if (!coord_set) continue;
                if (bwCoord.CancellationPending) return;
                bwCoord.ReportProgress(0);
            }
        }

        private void BwCoord_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            try
            {
                if (IsMouseOutside())
                    return;
                
                ShowCoord();
            }
            
            catch { }
        }

        private void AboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            About about = new About();
            about.Show();
        }

        private void ExitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Close(); 
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            this.Close();
        }

    }
}
