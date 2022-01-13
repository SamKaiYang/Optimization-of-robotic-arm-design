; Auto-generated. Do not edit!


(cl:in-package interface_control-msg)


;//! \htmlinclude dyna_data.msg.html

(cl:defclass <dyna_data> (roslisp-msg-protocol:ros-message)
  ((payload
    :reader payload
    :initarg :payload
    :type cl:float
    :initform 0.0)
   (payload_position
    :reader payload_position
    :initarg :payload_position
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (vel
    :reader vel
    :initarg :vel
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (acc
    :reader acc
    :initarg :acc
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass dyna_data (<dyna_data>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <dyna_data>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'dyna_data)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name interface_control-msg:<dyna_data> is deprecated: use interface_control-msg:dyna_data instead.")))

(cl:ensure-generic-function 'payload-val :lambda-list '(m))
(cl:defmethod payload-val ((m <dyna_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interface_control-msg:payload-val is deprecated.  Use interface_control-msg:payload instead.")
  (payload m))

(cl:ensure-generic-function 'payload_position-val :lambda-list '(m))
(cl:defmethod payload_position-val ((m <dyna_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interface_control-msg:payload_position-val is deprecated.  Use interface_control-msg:payload_position instead.")
  (payload_position m))

(cl:ensure-generic-function 'vel-val :lambda-list '(m))
(cl:defmethod vel-val ((m <dyna_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interface_control-msg:vel-val is deprecated.  Use interface_control-msg:vel instead.")
  (vel m))

(cl:ensure-generic-function 'acc-val :lambda-list '(m))
(cl:defmethod acc-val ((m <dyna_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interface_control-msg:acc-val is deprecated.  Use interface_control-msg:acc instead.")
  (acc m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <dyna_data>) ostream)
  "Serializes a message object of type '<dyna_data>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'payload))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'payload_position))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'payload_position))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'vel))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'acc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'acc))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <dyna_data>) istream)
  "Deserializes a message object of type '<dyna_data>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'payload) (roslisp-utils:decode-single-float-bits bits)))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'payload_position) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'payload_position)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'vel) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'vel)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'acc) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'acc)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<dyna_data>)))
  "Returns string type for a message object of type '<dyna_data>"
  "interface_control/dyna_data")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'dyna_data)))
  "Returns string type for a message object of type 'dyna_data"
  "interface_control/dyna_data")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<dyna_data>)))
  "Returns md5sum for a message object of type '<dyna_data>"
  "c2f6e80701d6dcd8d4e79d9988c813f6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'dyna_data)))
  "Returns md5sum for a message object of type 'dyna_data"
  "c2f6e80701d6dcd8d4e79d9988c813f6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<dyna_data>)))
  "Returns full string definition for message of type '<dyna_data>"
  (cl:format cl:nil "float32 payload~%float32[] payload_position~%float32[] vel~%float32[] acc~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'dyna_data)))
  "Returns full string definition for message of type 'dyna_data"
  (cl:format cl:nil "float32 payload~%float32[] payload_position~%float32[] vel~%float32[] acc~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <dyna_data>))
  (cl:+ 0
     4
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'payload_position) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'vel) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'acc) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <dyna_data>))
  "Converts a ROS message object to a list"
  (cl:list 'dyna_data
    (cl:cons ':payload (payload msg))
    (cl:cons ':payload_position (payload_position msg))
    (cl:cons ':vel (vel msg))
    (cl:cons ':acc (acc msg))
))
