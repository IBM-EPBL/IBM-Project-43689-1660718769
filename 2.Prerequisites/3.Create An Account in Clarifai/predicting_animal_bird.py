from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

USER_ID = 'kenywod'
PAT = 'ee987c2e88ad44a2ab7e8eaf747bbfc4'
APP_ID = '1a3587d95adb42a78d82d7a7247de69c'
MODEL_ID = 'general-image-recognition'
IMAGE_URL = 'https://portal.clarifai.com/users/kenywod/apps/1a3587d95adb42a78d82d7a7247de69c/explorer/inputs/a295623124e24327a3c2aaf47df28ae2'
CONCEPT_NAME = "bird"
CONCEPT_ID = "A295623124E24327A3C2AAF47DF28AE2"

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

post_model_outputs_response = stub.PostModelOutputs(
    service_pb2.PostModelOutputsRequest(
        user_app_id=userDataObject,
        model_id=MODEL_ID,  
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        url=IMAGE_URL
                    )
                )
            )
        ],
        model=resources_pb2.Model(
            output_info=resources_pb2.OutputInfo(
                output_config=resources_pb2.OutputConfig(
                    select_concepts=[
                        resources_pb2.Concept(name=CONCEPT_NAME),
                        resources_pb2.Concept(id=CONCEPT_ID)
                    ]
                )
            )
        )
    ),
    metadata=metadata
)
if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
    print(post_model_outputs_response.status)
    raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)


output = post_model_outputs_response.outputs[0]

print("Predicted concepts:")
for concept in output.data.concepts:
    print("%s %.2f" % (concept.name, concept.value))
