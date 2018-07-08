""" A Db4pkg class
Experiments on trying to generate package DB for ROOT PM
"""
import yaml
from generator.dbgenerator import *

class Db4pkg():
    def __init__(self, db_dict=None):
        """ initializes a db object
        """
        if db_dict == None:
            db_dict = {}
        self.__db_dict = db_dict

    def hardcoded_db(self):
        """ Hardcoded ROOT manifest
        """
        db_source = """
        ZLIB:
            path: builtins/zlib/
        Graf3d:
            deps: Graf Hist Gpad MathCore
            path: graf3d/g3d/
        Graf:
            deps: Hist Matrix MathCore
            path: graf2d/graf/
        Gpad:
            deps: Graf Hist
            path: graf2d/gpad/
        Hist:
            deps: MathCore Matrix
            path: hist/hist/
        Hbook:
            deps: Hist Matrix Tree Graf TreePlayer
            path: hist/hbook/
        ROOTHistDraw:
            deps: ROOTGraphicsPrimitives
            path: hist/histdraw/
        HistPainter:
            deps: Graf Hist Matrix MathCore ROOTHistDraw
            path: hist/histpainter/
        Spectrum:
            deps: Hist Matrix
            path: hist/spectrum/
        SpectrumPainter:
            deps: Graf Hist
            path: hist/spectrumpainter/
        Unfold:
            deps: Hist XMLParser Matrix
            path: hist/unfold/
        Tree:
            deps: Net MathCore
            path: tree/tree/
        ROOTDataFrame:
            deps: Tree TreePlayer Hist ROOTVecOps
            path: tree/dataframe/
        TreePlayer:
            deps: Tree Graf3d Graf Hist Gpad MathCore
            path: tree/treeplayer/
        XMLIO:
            path: io/xml/
        Net:
            path: net/net/
        XMLParser:
            path: io/xmlparser/
        SQLIO:
            deps: Net
            path: io/sql/
        RFIO:
            deps: Net
            path: io/rfio/
        HDFS:
            deps: Net
            path: io/hdfs/
        GFAL:
            deps: Net
            path: io/gfal/
        DCache:
            deps: Net
            path: io/dcache/
        RCastor:
            deps: Net
            path: io/castor/
        MathCore:
            path: math/mathcore/
        Matrix:
            deps: MathCore
            path: math/matrix/
        Quadp:
            deps: Matrix
            path: math/quadp/
        FFTW:
            deps: MathCore
            path: math/fftw/
        Fumili:
            deps: MathCore Hist Graf
            path: math/fumili/
        Foam:
            deps: MathCore Hist
            path: math/foam/
        Genetic:
            deps: MathCore TMVA
            path: math/genetic/
        GenVector:
            deps: MathCore Physics
            path: math/genvector/
        MathMore:
            deps: MathCore
            path: math/mathmore/
        Minuit:
            deps: Graf Hist Matrix MathCore
            path: math/minuit/
        Minuit2:
            deps: MathCore Hist
            path: math/minuit2/
        MLP:
            deps: Hist Matrix Tree Graf Gpad TreePlayer MathCore
            path: math/mlp/
        Physics:
            deps: Matrix MathCore
            path: math/physics/
        Rtools:
            deps: MathCore RInterface
            path: math/rtools/
        Smatrix:
            deps: Matrix MathCore
            path: math/smatrix/
        Splot:
            deps: Matrix Hist Tree TreePlayer Graf3d Graf MathCore
            path: math/splot/
        Unuran:
            deps: Hist MathCore
            path: math/unuran/
        ROOTVecOps:
            deps: Matrix
            path: math/vecops/
        TMVA:
            path:
        RInterface:
            path:
        ROOTGraphicsPrimitives:
            path:
        """
        db_manifest = yaml.load(db_source)
        return db_manifest

    def generated_manifest(self):
        if not os.path.exists('./manifest.yml'):
            print("[root-get] No manifest file..weird, please check what could be wrong with generation.")
            open('manifest.yml', 'a').close()
        DBgen = Dbgenerator()
        DBgen.dbgenerator()
        global db_value
        db_value = DBgen.clean_deps()
        db_manifest = []
        with open("manifest.yml") as stream:
            try:
                db_manifest = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return db_manifest

    def pre_dag(self, db_manifest):
        """ Removing not needed keys, needed step for DAG
            FIXME: will not be needed for generated manifests
        """
        pre_dag_db = {}
        try:
            for i in db_manifest:
                if 'deps' in db_manifest[i]:
                    if db_value == "deps":
                        pre_dag_db[i] = db_manifest[i]['deps'].split(' ')
                else:
                    pre_dag_db[i] = []
        except:
            pass
        return pre_dag_db
