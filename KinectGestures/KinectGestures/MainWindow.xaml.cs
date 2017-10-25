using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using LightBuzz.Vitruvius;
using Microsoft.Kinect;
using System.Net;
using System.IO;

namespace KinectGestures
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        KinectSensor sensor;
        MultiSourceFrameReader reader;
        GestureController gestureController;

        public MainWindow()
        {
            InitializeComponent();

            // Initialize
            sensor = KinectSensor.GetDefault();
            if (sensor != null)
            {
                sensor.Open();

                reader = sensor.OpenMultiSourceFrameReader(FrameSourceTypes.Color | FrameSourceTypes.Depth | FrameSourceTypes.Infrared | FrameSourceTypes.Body);
                reader.MultiSourceFrameArrived += Reader_MultiSourceFrameArrived;

                gestureController = new GestureController();
                gestureController.GestureRecognized += GestureController_GestureRecognized;
            }
        }

        void Reader_MultiSourceFrameArrived(object sender, MultiSourceFrameArrivedEventArgs e)
        {
            var reference = e.FrameReference.AcquireFrame();
            // Color
            using (var frame = reference.ColorFrameReference.AcquireFrame())
            {
                if (frame != null && viewer.Visualization == Visualization.Color)
                {
                    viewer.Image = frame.ToBitmap();
                }
            }
            // Body
            using (var frame = reference.BodyFrameReference.AcquireFrame())
            {
                if (frame != null)
                {
                    Body body = frame.Bodies().Closest();
                    if (body != null)
                    {
                        gestureController.Update(body);
                    }
                }
            }
        }

        void GestureController_GestureRecognized(object sender, GestureEventArgs e)
        {
            string gesture = e.GestureType.ToString();
            tblGestures.Text = gesture;
            //SendData(gesture);
        }

        void SendData()
        {
            string url = @"http://naokinect.azurewebsites.net/Data?sending=";
            string data = "test222";
            WebRequest.Create(url + data).GetResponse();

            /*
            WebRequest wrGETURL;
            wrGETURL = WebRequest.Create(url);
            
            using (Stream objStream = wrGETURL.GetResponse().GetResponseStream())
            {
                using (StreamReader objReader = new StreamReader(objStream))
                {
                    string sLine = "";
                    int i = 0;

                    while (sLine != null)
                    {
                        i++;
                        sLine = objReader.ReadLine();
                        if (sLine != null)
                            Console.WriteLine("{0}:{1}", i, sLine);
                    }
                    Console.ReadLine();
                }                    
            }
            */
        }
    }
}
