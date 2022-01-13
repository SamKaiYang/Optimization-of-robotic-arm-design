; Auto-generated. Do not edit!


(cl:in-package interface_control-msg)


;//! \htmlinclude cal_cmd.msg.html

(cl:defclass <cal_cmd> (roslisp-msg-protocol:ros-message)
  ((cmd
    :reader cmd
    :initarg :cmd
    :type cl:integer
    :initform 0))
)

(cl:defclass cal_cmd (<cal_cmd>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <cal_cmd>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'cal_cmd)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name interface_control-msg:<cal_cmd> is deprecated: use interface_control-msg:cal_cmd instead.")))

(cl:ensure-generic-function 'cmd-val :lambda-list '(m))
(cl:defmethod cmd-val ((m <cal_cmd>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader interface_control-msg:cmd-val is deprecated.  Use interface_control-msg:cmd instead.")
  (cmd m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <cal_cmd>) ostream)
  "Serializes a message object of type '<cal_cmd>"
  (cl:let* ((signed (cl:slot-value msg 'cmd)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <cal_cmd>) istream)
  "Deserializes a message object of type '<cal_cmd>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cmd) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<cal_cmd>)))
  "Returns string type for a message object of type '<cal_cmd>"
  "interface_control/cal_cmd")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'cal_cmd)))
  "Returns string type for a message object of type 'cal_cmd"
  "interface_control/cal_cmd")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<cal_cmd>)))
  "Returns md5sum for a message object of type '<cal_cmd>"
  "66990e73c7aab0c47ddcdc70f7fa5bd0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'cal_cmd)))
  "Returns md5sum for a message object of type 'cal_cmd"
  "66990e73c7aab0c47ddcdc70f7fa5bd0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<cal_cmd>)))
  "Returns full string definition for message of type '<cal_cmd>"
  (cl:format cl:nil "int32 cmd~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'cal_cmd)))
  "Returns full string definition for message of type 'cal_cmd"
  (cl:format cl:nil "int32 cmd~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <cal_cmd>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <cal_cmd>))
  "Converts a ROS message object to a list"
  (cl:list 'cal_cmd
    (cl:cons ':cmd (cmd msg))
))
