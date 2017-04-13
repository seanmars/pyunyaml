# -*- coding: utf-8 -*-

import glob
import os
import sys
from collections import OrderedDict

import better_exceptions
import ruamel.yaml
import yaml
from ruamel.yaml.comments import CommentedMap, CommentedOrderedMap
from yaml import SafeDumper

CLASS_ID_RAW = """1,GameObject
2,Component
3,LevelGameManager
4,Transform
5,TimeManager
6,GlobalGameManager
8,Behaviour
9,GameManager
11,AudioManager
12,ParticleAnimator
13,InputManager
15,EllipsoidParticleEmitter
17,Pipeline
18,EditorExtension
19,Physics2DSettings
20,Camera
21,Material
23,MeshRenderer
25,Renderer
26,ParticleRenderer
27,Texture
28,Texture2D
29,SceneSettings
30,GraphicsSettings
33,MeshFilter
41,OcclusionPortal
43,Mesh
45,Skybox
47,QualitySettings
48,Shader
49,TextAsset
50,Rigidbody2D
51,Physics2DManager
53,Collider2D
54,Rigidbody
55,PhysicsManager
56,Collider
57,Joint
58,CircleCollider2D
59,HingeJoint
60,PolygonCollider2D
61,BoxCollider2D
62,PhysicsMaterial2D
64,MeshCollider
65,BoxCollider
66,SpriteCollider2D
68,EdgeCollider2D
72,ComputeShader
74,AnimationClip
75,ConstantForce
76,WorldParticleCollider
78,TagManager
81,AudioListener
82,AudioSource
83,AudioClip
84,RenderTexture
87,MeshParticleEmitter
88,ParticleEmitter
89,Cubemap
90,Avatar
91,AnimatorController
92,GUILayer
93,RuntimeAnimatorController
94,ScriptMapper
95,Animator
96,TrailRenderer
98,DelayedCallManager
102,TextMesh
104,RenderSettings
108,Light
109,CGProgram
110,BaseAnimationTrack
111,Animation
114,MonoBehaviour
115,MonoScript
116,MonoManager
117,Texture3D
118,NewAnimationTrack
119,Projector
120,LineRenderer
121,Flare
122,Halo
123,LensFlare
124,FlareLayer
125,HaloLayer
126,NavMeshAreas
127,HaloManager
128,Font
129,PlayerSettings
130,NamedObject
131,GUITexture
132,GUIText
133,GUIElement
134,PhysicMaterial
135,SphereCollider
136,CapsuleCollider
137,SkinnedMeshRenderer
138,FixedJoint
140,RaycastCollider
141,BuildSettings
142,AssetBundle
143,CharacterController
144,CharacterJoint
145,SpringJoint
146,WheelCollider
147,ResourceManager
148,NetworkView
149,NetworkManager
150,PreloadData
152,MovieTexture
153,ConfigurableJoint
154,TerrainCollider
155,MasterServerInterface
156,TerrainData
157,LightmapSettings
158,WebCamTexture
159,EditorSettings
160,InteractiveCloth
161,ClothRenderer
162,EditorUserSettings
163,SkinnedCloth
164,AudioReverbFilter
165,AudioHighPassFilter
166,AudioChorusFilter
167,AudioReverbZone
168,AudioEchoFilter
169,AudioLowPassFilter
170,AudioDistortionFilter
171,SparseTexture
180,AudioBehaviour
181,AudioFilter
182,WindZone
183,Cloth
184,SubstanceArchive
185,ProceduralMaterial
186,ProceduralTexture
191,OffMeshLink
192,OcclusionArea
193,Tree
194,NavMeshObsolete
195,NavMeshAgent
196,NavMeshSettings
197,LightProbesLegacy
198,ParticleSystem
199,ParticleSystemRenderer
200,ShaderVariantCollection
205,LODGroup
206,BlendTree
207,Motion
208,NavMeshObstacle
210,TerrainInstance
212,SpriteRenderer
213,Sprite
214,CachedSpriteAtlas
215,ReflectionProbe
216,ReflectionProbes
218,Terrain
220,LightProbeGroup
221,AnimatorOverrideController
222,CanvasRenderer
223,Canvas
224,RectTransform
225,CanvasGroup
226,BillboardAsset
227,BillboardRenderer
228,SpeedTreeWindAsset
229,AnchoredJoint2D
230,Joint2D
231,SpringJoint2D
232,DistanceJoint2D
233,HingeJoint2D
234,SliderJoint2D
235,WheelJoint2D
238,NavMeshData
240,AudioMixer
241,AudioMixerController
243,AudioMixerGroupController
244,AudioMixerEffectController
245,AudioMixerSnapshotController
246,PhysicsUpdateBehaviour2D
247,ConstantForce2D
248,Effector2D
249,AreaEffector2D
250,PointEffector2D
251,PlatformEffector2D
252,SurfaceEffector2D
258,LightProbes
271,SampleClip
272,AudioMixerSnapshot
273,AudioMixerGroup
290,AssetBundleManifest
1001,Prefab
1002,EditorExtensionImpl
1003,AssetImporter
1004,AssetDatabase
1005,Mesh3DSImporter
1006,TextureImporter
1007,ShaderImporter
1008,ComputeShaderImporter
1011,AvatarMask
1020,AudioImporter
1026,HierarchyState
1027,GUIDSerializer
1028,AssetMetaData
1029,DefaultAsset
1030,DefaultImporter
1031,TextScriptImporter
1032,SceneAsset
1034,NativeFormatImporter
1035,MonoImporter
1037,AssetServerCache
1038,LibraryAssetImporter
1040,ModelImporter
1041,FBXImporter
1042,TrueTypeFontImporter
1044,MovieImporter
1045,EditorBuildSettings
1046,DDSImporter
1048,InspectorExpandedState
1049,AnnotationManager
1050,PluginImporter
1051,EditorUserBuildSettings
1052,PVRImporter
1053,ASTCImporter
1054,KTXImporter
1101,AnimatorStateTransition
1102,AnimatorState
1105,HumanTemplate
1107,AnimatorStateMachine
1108,PreviewAssetType
1109,AnimatorTransition
1110,SpeedTreeImporter
1111,AnimatorTransitionBase
1112,SubstanceImporter
1113,LightmapParameters
1120,LightmapSnapshot"""

CLASS_ID_DICT = {}

id_lines = CLASS_ID_RAW.splitlines()
for line in id_lines:
    tmp = line.split(',')
    CLASS_ID_DICT.update({tmp[1]: tmp[0]})


def get_class_id(class_name):
    class_name = class_name.replace(':', '')
    class_id = CLASS_ID_DICT.get(class_name, None)
    if class_id is None:
        raise TypeError('Class not found.')

    return class_id


def get_tag_alias(class_name):
    class_id = get_class_id(class_name)
    return '!u!{}'.format(class_id)


def get_object_id(value):
    return '&{}'.format(value)


def get_doc_title(alias, obj_id):
    return '--- {} {}'.format(alias, obj_id)


def remove_unity_TagAlias(filepath, ignore_id=False):
    """
    Name: remove_unity_TagAlias()

    Description: Loads a file object from a Unity textual scene file,
    which is in a pseudo YAML style, and strips the parts that are not YAML 1.1
    compliant. Then returns a string as a stream,
    which can be passed to PyYAML.
    Essentially removes the "!u!" tag directive,
    class type and the "&" file ID directive.
    PyYAML seems to handle rest just fine after that.

    Returns: String (YAML stream as string)
    """

    result = str()
    sourceFile = open(filepath, 'r')
    id_ = None
    for lineNumber, line in enumerate(sourceFile.readlines()):
        if line.startswith('--- !u!'):
            # remove the tag, but keep file ID
            result += '--- ' + line.split(' ')[2]
            if not ignore_id:
                id_ = (line.split(' ')[2]).replace('&', '')
        else:
            # Just copy the contents...
            result += line
            if id_:
                result += '  _tmp_id: {}'.format(id_)
                id_ = None
    sourceFile.close()

    return result


def remove_tmp_id(lines):
    new_lines = []
    for index, value in enumerate(lines):
        if '_tmp_id' in value:
            continue
        else:
            new_lines.append(value)

    return new_lines


def remove_redundant_tag(lines):
    new_lines = []
    for index, value in enumerate(lines):
        if index < 2:
            new_lines.append(value)
            continue
        if value.startswith('%YAML') or value.startswith('%TAG'):
            continue
        new_lines.append(value)

    return new_lines


def transform_to_unity_yaml(lines):
    result = str()
    tag_alias_str = str()
    doc_flag = False
    start_index = -1

    # make doc title
    for index, value in enumerate(lines):
        if doc_flag:
            if '_tmp_id' in value:
                spt_id = value.split(': ')
                id_str = get_object_id(spt_id[1])
                lines[start_index] = get_doc_title(
                    tag_alias_str, id_str)
                start_index = -1
                doc_flag = False
                continue
        else:
            if value.startswith('---'):
                start_index = index
                tag_alias_str = get_tag_alias(
                    lines[index + 1])
                doc_flag = True

    # remove
    result = remove_tmp_id(lines)
    result = remove_redundant_tag(result)

    return '\n'.join(result)


def sortOD(od, deep=0):
    if deep > 1:
        return od
    deep += 1
    res = CommentedMap()
    for k, v in sorted(od.items()):
        # print('{}: {}, {}: {}'.format(type(k), k, type(v), v))
        if isinstance(v, CommentedMap):
            res[k] = sortOD(v, deep)
        else:
            res[k] = v
    return res


def get_id(doc):
    for k, v in doc.items():
        return v['_tmp_id']


def output_sorted(filename, docs):
    sorted_docs = sorted(list(docs),
                         key=lambda doc: get_id(doc))

    outstr = yaml.safe_dump_all(sorted_docs,
                                indent=None,
                                encoding='utf-8',
                                allow_unicode=False,
                                version=(1, 1),
                                tags={'!u!': 'tag:unity3d.com,2011:'})
    outstr = outstr.decode("utf-8")
    final = transform_to_unity_yaml(outstr.splitlines())

    with open(filename, mode='w', encoding='utf-8') as wf:
        wf.write(final)


def output_sorted_by_ruamel(filename, docs):
    sorted_docs = sorted(list(docs),
                         key=lambda doc: get_id(doc))

    final_docs = []
    for d in sorted_docs:
        final_docs.append(sortOD(d))

    outstr = ruamel.yaml.dump_all(final_docs,
                                  Dumper=ruamel.yaml.RoundTripDumper,
                                  indent=None,
                                  encoding='utf-8',
                                  allow_unicode=False,
                                  version=(1, 1),
                                  tags={'!u!': 'tag:unity3d.com,2011:'})
    outstr = outstr.decode("utf-8")
    final = transform_to_unity_yaml(outstr.splitlines())
    # final = outstr

    with open(filename, mode='w', encoding='utf-8') as wf:
        wf.write(final)


def output_raw_by_ruamel(filename, docs):
    with open(filename, mode='w', encoding='utf-8') as wf:
        ruamel.yaml.dump_all(docs, stream=wf,
                             Dumper=ruamel.yaml.RoundTripDumper,
                             indent=None,
                             encoding='utf-8')


def transform(filename):
    SafeDumper.add_representer(
        type(None),
        lambda dumper, value: dumper.represent_scalar(
            u'tag:yaml.org,2002:null', '')
    )

    yamlstr = remove_unity_TagAlias(filename)
    docs = yaml.load_all(yamlstr, Loader=yaml.Loader)
    output_sorted(filename, docs)

    # docs = ruamel.yaml.load_all(yamlstr, ruamel.yaml.RoundTripLoader)
    # output_sorted_by_ruamel(filename, docs)
    # output_raw_by_ruamel(filename, docs)


def main():
    if len(sys.argv) < 2:
        print('Please give path.')
        exit()

    path = sys.argv[1]
    if not os.path.exists(path):
        print('Path not found.')
        exit()

    files = []
    cnt_prefab = 0
    cnt_unity = 0
    cnt_asset = 0
    for filename in glob.glob('{}/**/*.*'.format(path), recursive=True):
        if filename.endswith('.prefab'):
            files.append(filename)
            cnt_prefab += 1
        if filename.endswith('.unity'):
            files.append(filename)
            cnt_unity += 1
        if filename.endswith('.asset'):
            files.append(filename)
            cnt_asset += 1

    total = len(files)
    print('Total: {} (.prefab: {}, .unity: {}, .asset: {})'.format(
        total, cnt_prefab, cnt_unity, cnt_asset))
    count = 0
    for f in files:
        count += 1
        print('{}/{} => {}'.format(count, total, f))
        transform(f)

    print(total, 'done')


if __name__ == '__main__':
    main()
