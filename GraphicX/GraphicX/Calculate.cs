using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace GraphicX
{
    public partial class Main : Form
    {
        bool coord_set = false;

        const string VBS_file = "script.vbs";
        const string output_file = "output.txt";

        double xmin, xmax, xstep, ymin, ymax, min, max, range;

        string formula;

        List<double[]> values; // actual points on the curve
        List<double[]> values_perc; // points on the curve as percentages of width / height of the bmp_graph

        private bool GetParams()
        {
            // checks validity of user input

            formula = textBox_formula.Text;
            try
            {
                xmin = (double)Convert.ToDouble(textBox_xmin.Text);
                textBox_xmin.Text = xmin.ToString();
            }
            catch
            {
                MessageBox.Show("Invalid xmin");
                coord_set = false;
                return false;
            }
            try
            {
                xmax = (double)Convert.ToDouble(textBox_xmax.Text);
                textBox_xmax.Text = xmax.ToString();
            }
            catch
            {
                MessageBox.Show("Invalid xmax");
                coord_set = false;
                return false;
            }
            try
            {
                xstep = (double)Convert.ToDouble(textBox_xstep.Text);
                textBox_xstep.Text = xstep.ToString();
            }
            catch
            {
                MessageBox.Show("Invalid xstep");
                coord_set = false;
                return false;
            }
            if (xstep == 0)
            {
                MessageBox.Show("Invalid parameter: xstep = 0");
                coord_set = false;
                return false;
            }
            if (xmin > xmax && xstep > 0)
            {
                MessageBox.Show("Invalid parameters: xmin > xmax ; xstep > 0");
                coord_set = false;
                return false;
            }
            if (xmin < xmax && xstep < 0)
            {
                MessageBox.Show("Invalid parameters: xmax > xmin ; xstep < 0");
                coord_set = false;
                return false;
            }
            coord_set = true;
            return true;
        }

        private void CreateVBS()
        {
            // creates VBS script to calculate the graph points based on user input

            FileStream fs = new FileStream(VBS_file, FileMode.Create);
            StreamWriter sw = new StreamWriter(fs);

            sw.WriteLine("Const x_min = " + xmin.ToString().Replace(',', '.'));
            sw.WriteLine("Const x_max = " + xmax.ToString().Replace(',', '.'));
            sw.WriteLine("Const x_step = " + xstep.ToString().Replace(',', '.'));
            sw.WriteLine();
            sw.WriteLine("On Error Resume Next");
            sw.WriteLine("Dim fw: Set fw = CreateObject(\"Scripting.FileSystemObject\").OpenTextFile(\"" + output_file + "\",2,true)");
            sw.WriteLine();
            sw.WriteLine("Dim x, y");
            sw.WriteLine("For x = x_min To x_max Step x_step");
            sw.WriteLine("\ty = " + formula);
            sw.WriteLine("\tIf Err.Number <> 0 Then");
            sw.WriteLine("\t\tErr.Clear");
            sw.WriteLine("\t\tfw.Close");
            sw.WriteLine("\t\tSet fw = Nothing");
            sw.WriteLine("\t\tWScript.Quit 1");
            sw.WriteLine("\tEnd If");
            sw.WriteLine("\tfw.WriteLine CStr(x) & \" \" & CStr(y)");
            sw.WriteLine("Next");
            sw.WriteLine();
            sw.WriteLine("fw.Close");
            sw.WriteLine("Set fw = Nothing");
            sw.Close();
            fs.Close();
        }

        private List<double[]> CreateOutput()
        {
            // runs generated VBS code, and reads the output (points of graph)

            List<double[]> retValue = new List<double[]>();
            double[] tmp;

            string wscript = Environment.GetEnvironmentVariable("windir") + "\\SysWOW64\\wscript.exe";
            wscript = File.Exists(wscript) ? wscript : "wscript.exe";
            CreateVBS();
            Process p = new Process();
            p.StartInfo.FileName = wscript;
            p.StartInfo.Arguments = VBS_file;
            p.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            p.Start(); // run VBS
            p.WaitForExit();
            if (p.ExitCode > 0) // error
                return null;
            FileStream fs = new FileStream(output_file, FileMode.Open);
            StreamReader sr = new StreamReader(fs);
            string line;
            while (!sr.EndOfStream)
            {
                line = sr.ReadLine();
                try
                {
                    tmp = line.Split(' ').Select(x => double.Parse(x, CultureInfo.CurrentCulture)).ToArray();
                }
                catch
                {
                    return null;
                }
                retValue.Add(tmp);
            }
            sr.Close();
            fs.Close();

            return retValue;
        }

        private void CalcRange()
        {
            // calculates size of plotting area in coordinate system measures

            ymin = values.Min(x => x[1]);
            ymax = values.Max(x => x[1]);

            max = Math.Max(Math.Max(Math.Max(Math.Abs(xmin), Math.Abs(xmax)), Math.Abs(ymin)), Math.Abs(ymax));
            min = -1 * max;
            range = max - min;
        }
    }
}
