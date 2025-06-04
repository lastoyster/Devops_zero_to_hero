wait_for_instance(){
    local instance_id="$1"
    echo "Waiting for instance $instance_id to be ready..."

    while true; do 
    state=$(aws ec2 describe-instances --instance-ids "$instance_id" | jq -r '.Reservations[0].Instances[0].State.Name')
   if [ "$state" == "running" ]; then
    echo "Instance $instance_id is running."
    break
    fi 
    sleep 10
    done
}

create_ec2_instance(){
    local ami_id="$1"
    local instance_type="$2"
    local key_name ="$3"
    local subnet_id="$4"
    local security_group_id="$5"
    local instance_name="$6"

    instance_id=$(aws ec2 run-instances \
    --image-id "$ami_id" \
    --instance-type "$instance_type" \
    --key-name "$key_name" \

    --security-group-ids "$security_group_id" \ 
    --tag-specification "ResourceType=instance,Tags=[{Key=Name,Value=$instance_name}]" \
    --subnet-id "$subnet_id" \
    --query "Instances[0].InstanceId" \
    --output text
    )

    if [[-z "$instance_id"]]; then
    echo "Failed to create instance."
    exit 1
    fi

    echo "Instance $instance_id created successfully."

   wait_for_instance "$instance_id" 
}

main(){
   check_aws_cli || install_awscli 

   echo "creating ec2 instance"

   AMI_ID =""
   INSTANCE_TYPE="t2.micro"
   KEY_NAME=""
   SUBNET_ID=""
   SECURITY_GROUP_ID=""
   INSTANCE_NAME=""
   create_ec2_instance "$AMI_ID" "$INSTANCE_TYPE" "$KEY_NAME" "$SUBNET_ID" "$SECURITY_GROUP_ID" "$INSTANCE_NAME"
    echo  "EC2 instance creation completed."
}

main "$a"