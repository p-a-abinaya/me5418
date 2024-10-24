// Generated by gencpp from file kindr_msgs/VectorAtPosition.msg
// DO NOT EDIT!


#ifndef KINDR_MSGS_MESSAGE_VECTORATPOSITION_H
#define KINDR_MSGS_MESSAGE_VECTORATPOSITION_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <geometry_msgs/Vector3.h>
#include <geometry_msgs/Point.h>

namespace kindr_msgs
{
template <class ContainerAllocator>
struct VectorAtPosition_
{
  typedef VectorAtPosition_<ContainerAllocator> Type;

  VectorAtPosition_()
    : header()
    , type(0)
    , name()
    , vector()
    , position()
    , position_frame_id()  {
    }
  VectorAtPosition_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , type(0)
    , name(_alloc)
    , vector(_alloc)
    , position(_alloc)
    , position_frame_id(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef uint8_t _type_type;
  _type_type type;

   typedef std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> _name_type;
  _name_type name;

   typedef  ::geometry_msgs::Vector3_<ContainerAllocator>  _vector_type;
  _vector_type vector;

   typedef  ::geometry_msgs::Point_<ContainerAllocator>  _position_type;
  _position_type position;

   typedef std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> _position_frame_id_type;
  _position_frame_id_type position_frame_id;



// reducing the odds to have name collisions with Windows.h 
#if defined(_WIN32) && defined(TYPE_TYPELESS)
  #undef TYPE_TYPELESS
#endif
#if defined(_WIN32) && defined(TYPE_JERK)
  #undef TYPE_JERK
#endif
#if defined(_WIN32) && defined(TYPE_ACCELERATION)
  #undef TYPE_ACCELERATION
#endif
#if defined(_WIN32) && defined(TYPE_VELOCITY)
  #undef TYPE_VELOCITY
#endif
#if defined(_WIN32) && defined(TYPE_POSITION)
  #undef TYPE_POSITION
#endif
#if defined(_WIN32) && defined(TYPE_FORCE)
  #undef TYPE_FORCE
#endif
#if defined(_WIN32) && defined(TYPE_MOMEMTUM)
  #undef TYPE_MOMEMTUM
#endif
#if defined(_WIN32) && defined(TYPE_ANGULAR_JERK)
  #undef TYPE_ANGULAR_JERK
#endif
#if defined(_WIN32) && defined(TYPE_ANGULAR_ACCELERATION)
  #undef TYPE_ANGULAR_ACCELERATION
#endif
#if defined(_WIN32) && defined(TYPE_ANGULAR_VELOCITY)
  #undef TYPE_ANGULAR_VELOCITY
#endif
#if defined(_WIN32) && defined(TYPE_TORQUE)
  #undef TYPE_TORQUE
#endif
#if defined(_WIN32) && defined(TYPE_ANGULAR_MOMEMTUM)
  #undef TYPE_ANGULAR_MOMEMTUM
#endif

  enum {
    TYPE_TYPELESS = 0u,
    TYPE_JERK = 6u,
    TYPE_ACCELERATION = 7u,
    TYPE_VELOCITY = 8u,
    TYPE_POSITION = 9u,
    TYPE_FORCE = 10u,
    TYPE_MOMEMTUM = 11u,
    TYPE_ANGULAR_JERK = 12u,
    TYPE_ANGULAR_ACCELERATION = 13u,
    TYPE_ANGULAR_VELOCITY = 14u,
    TYPE_TORQUE = 16u,
    TYPE_ANGULAR_MOMEMTUM = 17u,
  };


  typedef boost::shared_ptr< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> const> ConstPtr;

}; // struct VectorAtPosition_

typedef ::kindr_msgs::VectorAtPosition_<std::allocator<void> > VectorAtPosition;

typedef boost::shared_ptr< ::kindr_msgs::VectorAtPosition > VectorAtPositionPtr;
typedef boost::shared_ptr< ::kindr_msgs::VectorAtPosition const> VectorAtPositionConstPtr;

// constants requiring out of line definition

   

   

   

   

   

   

   

   

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::kindr_msgs::VectorAtPosition_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::kindr_msgs::VectorAtPosition_<ContainerAllocator1> & lhs, const ::kindr_msgs::VectorAtPosition_<ContainerAllocator2> & rhs)
{
  return lhs.header == rhs.header &&
    lhs.type == rhs.type &&
    lhs.name == rhs.name &&
    lhs.vector == rhs.vector &&
    lhs.position == rhs.position &&
    lhs.position_frame_id == rhs.position_frame_id;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::kindr_msgs::VectorAtPosition_<ContainerAllocator1> & lhs, const ::kindr_msgs::VectorAtPosition_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace kindr_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
{
  static const char* value()
  {
    return "fcf32a1df9f6d53ef1926f20ce6b66e0";
  }

  static const char* value(const ::kindr_msgs::VectorAtPosition_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xfcf32a1df9f6d53eULL;
  static const uint64_t static_value2 = 0xf1926f20ce6b66e0ULL;
};

template<class ContainerAllocator>
struct DataType< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
{
  static const char* value()
  {
    return "kindr_msgs/VectorAtPosition";
  }

  static const char* value(const ::kindr_msgs::VectorAtPosition_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Vector type definition (based on Kindr definitions)\n"
"uint8 TYPE_TYPELESS=0\n"
"uint8 TYPE_JERK=6\n"
"uint8 TYPE_ACCELERATION=7\n"
"uint8 TYPE_VELOCITY=8\n"
"uint8 TYPE_POSITION=9\n"
"uint8 TYPE_FORCE=10\n"
"uint8 TYPE_MOMEMTUM=11\n"
"uint8 TYPE_ANGULAR_JERK=12\n"
"uint8 TYPE_ANGULAR_ACCELERATION=13\n"
"uint8 TYPE_ANGULAR_VELOCITY=14\n"
"uint8 TYPE_TORQUE=16\n"
"uint8 TYPE_ANGULAR_MOMEMTUM=17\n"
"\n"
"std_msgs/Header header\n"
"uint8 type\n"
"string name\n"
"geometry_msgs/Vector3 vector # Frame defined in header\n"
"geometry_msgs/Point position # Point of origin of the vector\n"
"string position_frame_id # If empty same as vector frame\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Vector3\n"
"# This represents a vector in free space. \n"
"# It is only meant to represent a direction. Therefore, it does not\n"
"# make sense to apply a translation to it (e.g., when applying a \n"
"# generic rigid transformation to a Vector3, tf2 will only apply the\n"
"# rotation). If you want your data to be translatable too, use the\n"
"# geometry_msgs/Point message instead.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
;
  }

  static const char* value(const ::kindr_msgs::VectorAtPosition_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.type);
      stream.next(m.name);
      stream.next(m.vector);
      stream.next(m.position);
      stream.next(m.position_frame_id);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct VectorAtPosition_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::kindr_msgs::VectorAtPosition_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::kindr_msgs::VectorAtPosition_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "type: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.type);
    s << indent << "name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.name);
    s << indent << "vector: ";
    s << std::endl;
    Printer< ::geometry_msgs::Vector3_<ContainerAllocator> >::stream(s, indent + "  ", v.vector);
    s << indent << "position: ";
    s << std::endl;
    Printer< ::geometry_msgs::Point_<ContainerAllocator> >::stream(s, indent + "  ", v.position);
    s << indent << "position_frame_id: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.position_frame_id);
  }
};

} // namespace message_operations
} // namespace ros

#endif // KINDR_MSGS_MESSAGE_VECTORATPOSITION_H
