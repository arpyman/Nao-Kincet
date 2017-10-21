using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace NaoKinectWebApp
{
    public partial class Data : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            string gesture = Request.QueryString["sending"]; // Receive gesture from Kinect app
            if (gesture == null)
            {
                Response.Write(GlobalStorage.Gesture);
                Response.End();
            }
            else
            {
                GlobalStorage.Gesture = gesture;
                Response.Write("Gesture saved");
                Response.End();
            }
        }
    }
}