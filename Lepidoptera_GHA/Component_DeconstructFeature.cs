using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Lepidoptera;
using Lepidoptera_IO_Rhino;
using Lepidoptera_GHA.Properties;
using Newtonsoft.Json;
using System.IO;



namespace Lepidoptera_GHA
{
    public class LO_DeconstructFeature : GH_Component
    {
        public LO_DeconstructFeature()
            : base(nameof(LO_DeconstructFeature), "dF", "Deconstruct a Lepidoptera Feature", "Lepidoptera", "Regional Analysis")
        {
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("Feature", "F", "A Lepidoptera Feature to Deconstruct", GH_ParamAccess.item);
        }

        private static int IN_Feature = 0;
        private static int OUT_Geometry = 0;
        private static int OUT_Properties = 1;
        private static int OUT_IsValid = 2;

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.AddGeometryParameter("Geometry", "G", "The Feature's geometry.", GH_ParamAccess.list);
            pManager.AddGenericParameter("Properties", "P", "The Feature's Sentinal-2 Cell Properties (bands)", GH_ParamAccess.item);
            pManager.AddBooleanParameter("IsValid", "iV", "True if Feature is Valid", GH_ParamAccess.item);
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            LO_DeconstructFeature.DeonstructFeatureFromDA(DA);
        }

        protected override System.Drawing.Bitmap Icon => Resources.Lepidoptera;
        public override Guid ComponentGuid => new Guid("22dc4117-4786-45be-9f88-8e9eddfd08a8");
        private static void DeonstructFeatureFromDA(IGH_DataAccess DA)
        {
            FeatureGoo featureGoo = new FeatureGoo();

            if (!DA.GetData<Lepidoptera.FeatureGoo>(IN_Feature, ref featureGoo)) { return; }

            S2CellGoo s2Goo = new S2CellGoo(featureGoo.Value.properties);

            Point3d point = new Point3d(featureGoo.Value.geometry.coordinates[0], featureGoo.Value.geometry.coordinates[1], 0);

            DA.SetData(OUT_Geometry, point);
            DA.SetData(OUT_Properties, s2Goo);
            DA.SetData(OUT_IsValid, featureGoo.Value.IsValid);
        }
    }
}