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
            if (HttpContext.Current.Request.HttpMethod == "POST")
            {
                string incoming = Request.Form["data"]; // Receive Data from data variable
                if (incoming != null)
                {
                    GlobalStorage.Gesture = incoming;
                    Response.Write("Data saved");
                    Response.End();
                }
            }
            if (HttpContext.Current.Request.HttpMethod == "GET")
            {
                Response.Write(GlobalStorage.Gesture);
                Response.End();
            }
        }
    }
}