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
using System.Diagnostics;
using System.Collections.Specialized;
using System.Net.Http;

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
                    viewer.Clear();
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
                        viewer.DrawBody(body);
                    }
                }
            }
        }

        void GestureController_GestureRecognized(object sender, GestureEventArgs e)
        {
            //Gestures:
            //  JoinedHands	 0	 Hands joined in front of chest.
            //  WaveRight    1   Waving using the right hand.
            //  WaveLeft     2   Waving using the left hand.
            //  Menu         3   Hand slightly bent above hip(XBOX - like gesture).
            //  SwipeLeft    4   Hand moved horizontally from right to left.
            //  SwipeRight   5   Hand moved horizontally from left to right.
            //  SwipeUp      6   Hand moved vertically from hip center to head.
            //  SwipeDown    7   Hand moved vertically from head to hip center.
            //  ZoomIn       8   Both hands extended closer to the chest.
            //  ZoomOut      9	 Both hands extended farther from the chest.
            string gesture = e.GestureType.ToString();
            tblGestures.Text = gesture.ToString();
            Task.Run(() => SendData(gesture.ToString())); 
        }

        static async Task SendData(string data) // Send data using HTTP POST
        {
            Uri uri = new Uri(@"http://naokinect.azurewebsites.net/Data");

            using (HttpClient client = new HttpClient())
            {
                var content = new FormUrlEncodedContent(new[] { new KeyValuePair<string, string>("data", data) });
                var result = await client.PostAsync(uri, content);
                string resultContent = await result.Content.ReadAsStringAsync();
                Debug.WriteLine(resultContent);
            }

        }
    }
}
