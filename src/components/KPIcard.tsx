interface Props{
  title:string;
  value:string|number;
  color:string;
}

export default function KPIcard({title,value,color}:Props){

  return(

    <div className="bg-white rounded-2xl shadow-md p-5 border-l-8"
         style={{borderColor:color}}>

      <p className="text-gray-500 text-sm">{title}</p>

      <h2 className="text-3xl font-bold mt-2"
          style={{color}}>
        {value}
      </h2>

    </div>

  );

}