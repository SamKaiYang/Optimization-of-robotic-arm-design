;; Auto-generated. Do not edit!


(when (boundp 'interface_control::dyna_space_data)
  (if (not (find-package "INTERFACE_CONTROL"))
    (make-package "INTERFACE_CONTROL"))
  (shadow 'dyna_space_data (find-package "INTERFACE_CONTROL")))
(unless (find-package "INTERFACE_CONTROL::DYNA_SPACE_DATA")
  (make-package "INTERFACE_CONTROL::DYNA_SPACE_DATA"))

(in-package "ROS")
;;//! \htmlinclude dyna_space_data.msg.html


(defclass interface_control::dyna_space_data
  :super ros::object
  :slots (_payload _payload_position _vel _acc _joint_limits _analysis_axis ))

(defmethod interface_control::dyna_space_data
  (:init
   (&key
    ((:payload __payload) 0.0)
    ((:payload_position __payload_position) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:vel __vel) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:acc __acc) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_limits __joint_limits) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:analysis_axis __analysis_axis) 0)
    )
   (send-super :init)
   (setq _payload (float __payload))
   (setq _payload_position __payload_position)
   (setq _vel __vel)
   (setq _acc __acc)
   (setq _joint_limits __joint_limits)
   (setq _analysis_axis (round __analysis_axis))
   self)
  (:payload
   (&optional __payload)
   (if __payload (setq _payload __payload)) _payload)
  (:payload_position
   (&optional __payload_position)
   (if __payload_position (setq _payload_position __payload_position)) _payload_position)
  (:vel
   (&optional __vel)
   (if __vel (setq _vel __vel)) _vel)
  (:acc
   (&optional __acc)
   (if __acc (setq _acc __acc)) _acc)
  (:joint_limits
   (&optional __joint_limits)
   (if __joint_limits (setq _joint_limits __joint_limits)) _joint_limits)
  (:analysis_axis
   (&optional __analysis_axis)
   (if __analysis_axis (setq _analysis_axis __analysis_axis)) _analysis_axis)
  (:serialization-length
   ()
   (+
    ;; float64 _payload
    8
    ;; float32[] _payload_position
    (* 4    (length _payload_position)) 4
    ;; float32[] _vel
    (* 4    (length _vel)) 4
    ;; float32[] _acc
    (* 4    (length _acc)) 4
    ;; float32[] _joint_limits
    (* 4    (length _joint_limits)) 4
    ;; int32 _analysis_axis
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _payload
       (sys::poke _payload (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float32[] _payload_position
     (write-long (length _payload_position) s)
     (dotimes (i (length _payload_position))
       (sys::poke (elt _payload_position i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[] _vel
     (write-long (length _vel) s)
     (dotimes (i (length _vel))
       (sys::poke (elt _vel i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[] _acc
     (write-long (length _acc) s)
     (dotimes (i (length _acc))
       (sys::poke (elt _acc i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[] _joint_limits
     (write-long (length _joint_limits) s)
     (dotimes (i (length _joint_limits))
       (sys::poke (elt _joint_limits i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; int32 _analysis_axis
       (write-long _analysis_axis s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _payload
     (setq _payload (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float32[] _payload_position
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _payload_position (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _payload_position i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32[] _vel
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _vel (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _vel i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32[] _acc
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _acc (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _acc i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32[] _joint_limits
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_limits (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_limits i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; int32 _analysis_axis
     (setq _analysis_axis (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get interface_control::dyna_space_data :md5sum-) "505831417ccc6ae5a2e31ba38a82a2b6")
(setf (get interface_control::dyna_space_data :datatype-) "interface_control/dyna_space_data")
(setf (get interface_control::dyna_space_data :definition-)
      "float64 payload
float32[] payload_position
float32[] vel
float32[] acc
float32[] joint_limits
int32 analysis_axis

")



(provide :interface_control/dyna_space_data "505831417ccc6ae5a2e31ba38a82a2b6")


